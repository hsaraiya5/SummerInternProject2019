import urllib2
import json
import datetime
import csv
import time

def unicode_normalize(text):
    return text.translate({ 0x2018:0x27, 0x2019:0x27, 0x201C:0x22, 0x201D:0x22,
                            0xa0:0x20 }).encode('utf-8')

def request_data_from_url(url):
    req = urllib2.Request(url)
    success = False
    while success is False:
        try: 
            #open the url
            response = urllib2.urlopen(req)
            
            #200 is the success code for http
            if response.getcode() == 200:
                success = True
        except Exception, e:
            #if we didn't get a success, then print the error and wait 5 seconds before trying again
            print e
            time.sleep(5)

            print "Error for URL %s: %s" % (url, datetime.datetime.now())
            print "Retrying..."

    #return the contents of the response
    return response.read()

def get_facebook_page_data(page_id, access_token):

    website = "https://graph.facebook.com/v2.6/"
    
    location = "%s/posts/" % page_id 
    
    #the .limit(0).summary(true) is used to get a summarized count of all the ... 
    #...comments and reactions instead of getting each individual one
    fields = "?fields=message,created_time,type,name,id," + \
            "comments.limit(0).summary(true),shares," + \
            "reactions.limit(0).summary(true)"
            
    authentication = "&limit=100&access_token=%s" % (access_token)
    
    request_url = website + location + fields + authentication

    #converts facebook's response to a python dictionary to easier manipulate later
    data = json.loads(request_data_from_url(request_url))
    return data

def process_post(post, access_token):

    post_id = post['id']
    
    post_message = '' if 'message' not in post.keys() else \
            unicode_normalize(post['message'])
        
    post_type = post['type']

    #for datetime info, we need a few extra steps
    #first convert the given datetime into the format we want
    post_published = datetime.datetime.strptime(
            post['created_time'],'%Y-%m-%dT%H:%M:%S+0000')
    #then account for the time difference between the returned time and my time zone
    post_published = post_published + \
            datetime.timedelta(hours=-2)
    #last, convert the datetime into a string in a format convenient for spreadsheets
    post_published = post_published.strftime(
            '%Y-%m-%d %H:%M:%S')

    num_reactions = 0 if 'reactions' not in post else \
            post['reactions']['summary']['total_count']
    num_comments = 0 if 'comments' not in post else \
            post['comments']['summary']['total_count']
    num_shares = 0 if 'shares' not in post else post['shares']['count']

    #here we call a separate API for information about reactions based on the post's post_id
    #but only if this post is afer the day when reactions first appeared on facebook
    reactions = get_reactions_for_post(post_id, access_token) if \
            post_published > '2016-02-24 00:00:00' else {}

    num_likes = 0 if 'like' not in reactions else \
            reactions['like']['summary']['total_count']

    #if this post is from before reactions existed, then simply set the number of likes ...
    #...equal to the total number of reactions
    num_likes = num_reactions if post_published < '2016-02-24 00:00:00' \
            else num_likes

    #function to get total number of reactions from the reactions dictionary above
    def get_num_total_reactions(reaction_type, reactions):
        if reaction_type not in reactions:
            return 0
        else:
            return reactions[reaction_type]['summary']['total_count']

    #get counts of all reactions
    num_loves = get_num_total_reactions('love', reactions)
    num_wows = get_num_total_reactions('wow', reactions)
    num_hahas = get_num_total_reactions('haha', reactions)
    num_sads = get_num_total_reactions('sad', reactions)
    num_angrys = get_num_total_reactions('angry', reactions)

    #return a list of all the fields we asked for
    return (post_id, post_message, post_type,
            post_published, num_reactions, num_comments, num_shares,
            num_likes, num_loves, num_wows, num_hahas, num_sads, num_angrys)

def get_reactions_for_post(post_id, access_token):

    website = "https://graph.facebook.com/v2.6"
    
    location = "/%s" % post_id
    
    #here we ask for the number of reactions of each time associated with this post
    reactions = "/?fields=" \
            "reactions.type(LIKE).limit(0).summary(total_count).as(like)" \
            ",reactions.type(LOVE).limit(0).summary(total_count).as(love)" \
            ",reactions.type(WOW).limit(0).summary(total_count).as(wow)" \
            ",reactions.type(HAHA).limit(0).summary(total_count).as(haha)" \
            ",reactions.type(SAD).limit(0).summary(total_count).as(sad)" \
            ",reactions.type(ANGRY).limit(0).summary(total_count).as(angry)"
    
    authentication = "&access_token=%s" % access_token
    
    request_url = website + location + reactions + authentication

    # retrieve data and store in python dictionary
    data = json.loads(request_data_from_url(request_url))
     
    return data

def scrape_facebook_page(page_id, access_token):
    #open up a csv (comma separated values) file to write data to
    with open('%s_facebook_posts.csv' % page_id, 'wb') as file:
        #let w represent our file
        w = csv.writer(file)
        
        #write the header row
        w.writerow(["post_id", "post_message", "post_type",
                    "post_published", "num_reactions", 
                    "num_comments", "num_shares", "num_likes", "num_loves", 
                    "num_wows", "num_hahas", "num_sads", "num_angrys"])

        has_next_page = True
        num_processed = 0  
        scrape_starttime = datetime.datetime.now()

        print "Scraping %s Facebook Page: %s\n" % (page_id, scrape_starttime)

        #get first batch of posts
        posts = get_facebook_page_data(page_id, access_token)

        #while there is another page of posts to process
        while has_next_page:
            #we just limit to 200 posts for simplicity, if you want all the posts, just remove this
            if num_processed == 200:
                break
                
            #for each individual post in our retrieved posts ...
            for post in posts['data']:

                #...get post info and write to our spreadsheet
                w.writerow(process_post(post, access_token))
                    
                num_processed += 1

            #if there is a next page of posts to get, then get next page to process
            if 'paging' in posts.keys():
                posts = json.loads(request_data_from_url(
                                        posts['paging']['next']))
            #otherwise, we are done!
            else:
                has_next_page = False


        print "Completed!\n%s posts Processed in %s" % \
                (num_processed, datetime.datetime.now() - scrape_starttime)



    
scrape_facebook_page("marvelstudios", "EAAGM66M7I6IBANZAE978jU3TN2Qjs8uyezSNHW3YML5EnvJEcZC7DZBipubPpvfZCqwTEMgU3d9AdG7LbqbyX54WQZBGnAkEDJHFRG7VTYBUGnVI6QSLcWxtGWCjRS0JZAO2umDZAJtqiqG6pFten5zuklsceHUGdTQvSEmtWDWiqhKwGdi2ZAjyeSEsEHuXeCgt849w2NXyErbNg53i2yZB8")