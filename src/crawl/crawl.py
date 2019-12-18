import sys
import twint
# Solve compatibility issues with notebooks and RunTime errors.
import nest_asyncio
nest_asyncio.apply()

def config(config,cmd):
	if( "-username" in cmd ):
		config.Username=cmd['-username']
	if( "-user_id" in cmd ):
		config.User_id=cmd['-user_id']
	if( "-search" in cmd ):
		config.Search=cmd['-search']
	if( "-geo" in cmd ):
		config.Geo=cmd['-geo']
	if( "-location" in cmd ):
		config.Location=cmd['-location']
	if( "-near" in cmd ):
		config.Near=cmd['-near']
	if( "-lang" in cmd ):
		config.Lang=cmd['-lang']
	if( "-output" in cmd ):
		config.Output=cmd['-output']
	if( "-elasticsearch" in cmd ):
		config.Elasticsearch=cmd['-elasticsearch']
	if( "-year" in cmd ):
		config.Year=cmd['-year']
	if( "-since" in cmd ):
		config.Since=cmd['-since']
	if( "-until" in cmd ):
		config.Until=cmd['-until']
	if( "-email" in cmd ):
		config.Email=cmd['-email']
	if( "-phone" in cmd ):
		config.Phone=cmd['-phone']
	if( "-verified" in cmd ):
		config.Verified=cmd['-verified']
	if( "-store_csv" in cmd ):
		config.Store_csv=cmd['-store_csv']
	if( "-store_json" in cmd ):
		config.Store_json=cmd['-store_json']
	if( "-custom" in cmd ):
		config.Custom=cmd['-custom']
	if( "-show_hashtags" in cmd ):
		config.Show_hashtags=cmd['-show_hashtags']
	if( "-limit" in cmd ):
		config.Limit=cmd['-limit']
	if( "-count" in cmd ):
		config.Count=cmd['-count']
	if( "-stats" in cmd ):
		config.Stats=cmd['-stats']
	if( "-database" in cmd ):
		config.Database=cmd['-database']
	if( "-to" in cmd ):
		config.To=cmd['-to']
	if( "-all" in cmd ):
		config.All=cmd['-all']
	if( "-debug" in cmd ):
		config.Debug=cmd['-debug']
	if( "-format" in cmd ):
		config.Format=cmd['-format']
	if( "-essid" in cmd ):
		config.Essid=cmd['-essid']
	if( "-user_full" in cmd ):
		config.User_full=cmd['-user_full']
	if( "-profile_full" in cmd ):
		config.Profile_full=cmd['-profile_full']
	if( "-store_object" in cmd ):
		config.Store_object=cmd['-store_object']
	if( "-store_pandas" in cmd ):
		config.Store_pandas=cmd['-store_pandas']
	if( "-pandas_type" in cmd ):
		config.Pandas_type=cmd['-pandas_type']
	if( "-pandas" in cmd ):
		config.Pandas=cmd['-pandas']
	if( "-index_tweets" in cmd ):
		config.Index_tweets=cmd['-index_tweets']
	if( "-index_follow" in cmd ):
		config.Index_follow=cmd['-index_follow']
	if( "-index_users" in cmd ):
		config.Index_users=cmd['-index_users']
	if( "-retries_count" in cmd ):
		config.Retries_count=int(cmd['-retries_count'])
	if( "-resume" in cmd ):
		config.Resume=cmd['-resume']
	if( "-images" in cmd ):
		config.Images=cmd['-images']
	if( "-videos" in cmd ):
		config.Videos=cmd['-videos']
	if( "-media" in cmd ):
		config.Media=cmd['-media']
	if( "-pandas_clean" in cmd ):
		config.Pandas_clean=cmd['-pandas_clean']
	if( "-lowercase" in cmd ):
		config.Lowercase=cmd['-lowercase']
	if( "-pandas_au" in cmd ):
		config.Pandas_au=cmd['-pandas_au']
	if( "-proxy_host" in cmd ):
		config.Proxy_host=cmd['-proxy_host']
	if( "-proxy_port" in cmd ):
		config.Proxy_port=cmd['-proxy_port']
	if( "-proxy_type" in cmd ):
		config.Proxy_type=cmd['-proxy_type']
	if( "-tor_control_port" in cmd ):
		config.Tor_control_port=cmd['-tor_control_port']
	if( "-tor_control_password" in cmd ):
		config.Tor_control_password=cmd['-tor_control_password']
	if( "-retweets" in cmd ):
		config.Retweets=cmd['-retweets']
	if( "-hide_output" in cmd ):
		config.Hide_output=cmd['-hide_output']
	if( "-popular_tweets" in cmd ):
		config.Popular_tweets=cmd['-popular_tweets']
	if( "-skip_certs" in cmd ):
		config.Skip_certs=cmd['-skip_certs']
	if( "-native_retweets" in cmd ):
		config.Native_retweets=cmd['-native_retweets']
	if( "-min_likes" in cmd ):
		config.Min_likes=cmd['-min_likes']
	if( "-min_retweets" in cmd ):
		config.Min_retweets=cmd['-min_retweets']
	if( "-min_replies" in cmd ):
		config.Min_replies=cmd['-min_replies']
	if( "-links" in cmd ):
		config.Links=cmd['-links']
	if( "-source" in cmd ):
		config.Source=cmd['-source']
	if( "-members_list" in cmd ):
		config.Members_list=cmd['-members_list']
	if( "-filter_retweets" in cmd ):
		config.Filter_retweets=cmd['-filter_retweets']
	return config

def crawl(c):
	twint.run.Search(c)

def main():

	counter=1
	cmd={}
	# for get cmd with -flag
	for cmdLine in sys.argv[1:]:
		if(cmdLine[:1]=='-' and counter+1<len(sys.argv)):
			cmd[cmdLine]=sys.argv[counter+1]
		counter+=1

	if('--help' in cmd):
		print("please see default config from twint , all cmd params in lower case")
		return 1

	# Set up TWINT config
	c = twint.Config()
	c = config(c,cmd)
	crawl(c)

main()