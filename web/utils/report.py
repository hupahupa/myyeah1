from flask import current_app
from web.models.user import User
from web.utils.report import *
import requests
import json

# GATHER REPORT DATA
def gather_dailymotion_report(v):
    return {}

def gather_youtube_report(v):
    YT_API_KEY = current_app.config["YT_API_KEY"]
    yt_url = "https://www.googleapis.com/youtube/v3/videos?part=statistics&id=%s&myrating=dislike&key=%s" % (v.yt_video_id, YT_API_KEY)
    print yt_url
    yt_resp = requests.get(yt_url).text
    yt_resp = json.loads(yt_resp)
    return format_youtube_data(yt_resp)

def gather_facebook_report(v):
    access = current_app.config["FB_ACCESS_TOKEN"]
    url='https://graph.facebook.com/'+str(v.fb_video_id)+'/video_insights?access_token='+str(access)
    # print url
    resp = requests.get(url).text
    resp = json.loads(resp)
    return format_facebook_data(resp)

# FORMAT DATA
def format_youtube_data(resp):
    d = []
    data = resp.get("items")[0].get("statistics")
    d.append(("view_count", data.get("viewCount")))
    d.append(("like_count", data.get("likeCount")))
    d.append(("dislike_count", data.get("dislikeCount")))
    d.append(("favorite_count", data.get("favoriteCount")))
    d.append(("comment_count", data.get("commentCount")))
    return d

def format_facebook_data(resp):
    # access value for single
    single = [
        "total_video_views",
        "total_video_views_unique",
        "total_video_views_autoplayed",
        "total_video_views_clicked_to_play",
        "total_video_views_organic",
        "total_video_views_organic_unique",
        "total_video_views_paid",
        "total_video_views_paid_unique",
        "total_video_views_sound_on",
        "total_video_complete_views",
        "total_video_complete_views_unique",
        "total_video_complete_views_auto_played",
        "total_video_complete_views_clicked_to_play",
        "total_video_complete_views_organic",
        "total_video_complete_views_organic_unique",
        "total_video_complete_views_paid",
        "total_video_complete_views_paid_unique",
        "total_video_10s_views",
        "total_video_10s_views_unique",
        "total_video_10s_views_auto_played",
        "total_video_10s_views_clicked_to_play",
        "total_video_10s_views_organic",
        "total_video_10s_views_paid",
        "total_video_10s_views_sound_on",
        "total_video_avg_time_watched",
        "total_video_view_total_time",
        "total_video_view_total_time_organic",
        "total_video_view_total_time_paid",
        "total_video_impressions",
        "total_video_impressions_unique",
        "total_video_impressions_paid_unique",
        "total_video_impressions_paid",
        "total_video_impressions_organic_unique",
        "total_video_impressions_organic",
        "total_video_impressions_viral_unique",
        "total_video_impressions_viral",
        "total_video_impressions_fan_unique",
        "total_video_impressions_fan",
        "total_video_impressions_fan_paid_unique",
        "total_video_impressions_fan_paid"
    ]
    # total_video_views_by_distribution_type
    # total_video_view_time_by_distribution_type
    # total_video_view_time_by_region_id (empty)
    # total_video_view_time_by_age_bucket_and_gender (empty)
    # total_video_retention_graph
    # total_video_retention_graph_autoplayed
    # total_video_retention_graph_clicked_to_play (empty
    # total_video_stories_by_action_type
    # total_video_reactions_by_type_total

    d = []
    for s in resp.get("data"):
        values = s.get("values")
        val = values[0]
        k = s.get("name")
        if (k in single):
            v = val.get("value")
            d.append((k, v))
        else:
            pass
    return d