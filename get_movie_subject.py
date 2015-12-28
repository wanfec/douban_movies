#!/usr/bin/env python
#coding=utf8

import httplib
import json
import time
import re

#get request in douban api
def doubanGet(uri):
    httpClient = None
    try:
        httpClient = httplib.HTTPConnection('api.douban.com', timeout=30)
        httpClient.request('GET', uri)

        #response是HTTPResponse对象
        response = httpClient.getresponse()
        list = response.read()
        return list
    except Exception, e:
        print Exception, ":", e
    finally:
        if httpClient:
            httpClient.close()

#get movies in theaters, the result is in jason
def getJson(file):
    fo01 = open(file, 'w')
    fo01.write(doubanGet('/v2/movie/in_theaters'))

#get id from the json
def getID(filein, fileout):
    fi01 = open(filein, 'r')
    fo01 = open(fileout, 'w')
    obj = fi01.read()
    decodejson = json.loads(obj)
    print type(decodejson)
    movienum = int(decodejson["count"])
    for i in range(movienum):
        print decodejson["subjects"][i]["id"]
        fo01.write(decodejson["subjects"][i]["id"] + '\n')

#get subject of a movie using movie id
def getMoviebyID(movieid):
    return doubanGet('/v2/movie/subject/'+movieid)

#get subjects of movies using movie ids from a file that contains the ids
def getMovies(filein, fileout):
    fi01 = open(filein, 'r')
    fo01 = open(fileout, 'w')
    i = 0;
    for line in fi01:
        starttime2=time.time()
        line = line.strip()
        fo01.write(getMoviebyID(line) + '\n')
        endtime2=time.time()
        print "抓取第%d页完毕，用时%.2fs"%(i+1,endtime2-starttime2)     #输出抓取每个页面所花费的时间
        time.sleep(2)
        i = i+1

def getMovieIDFromHTML(filein, fileout):
    fi01 = open(filein, 'r')
    fo01 = open(fileout, 'w')
    starttime2=time.time()
    for line in fi01:
        url = line.strip().split("\t")[1]
        movieID = re.search("subject/(\d+)",url).group(1)
        print(movieID)
        fo01.write(movieID + "\n")

def removeDuplicate(filein, fileout):
    fi01 = open(filein, 'r')
    fo01 = open(fileout, 'w')
    id_list = []
    for line in fi01:
        id_list.append((line.strip()))
    distinct_id_list = set(id_list)
    for id in distinct_id_list:
        fo01.write(id + '\n')

def getMovieFeatures(filein, fileout):
    fi01 = open(filein, 'r')
    fo01 = open(fileout, 'w')
    for line in fi01:
        decodejson = json.loads(line)
        features = []
        features.append(decodejson["id"])
        features.append(decodejson["title"].encode('utf-8'))
        features.append(decodejson["original_title"].encode('utf-8'))
        features.append(decodejson["ratings_count"])
        features.append(decodejson["wish_count"])
        features.append(decodejson["collect_count"])
        features.append(decodejson["subtype"])
        features.append(decodejson["directors"][0]["id"])
        features.append(decodejson["directors"][0]["name"].encode('utf-8'))
        features.append(decodejson["casts"][0]["id"])
        features.append(decodejson["casts"][0]["name"].encode('utf-8'))
        features.append(decodejson["year"])
        features.append(decodejson["countries"][0].encode('utf-8'))
        features.append(decodejson["comments_count"])
        features.append(decodejson["reviews_count"])
        for feature in features:
            print(feature)
            fo01.write(str(feature) + '\t')
        fo01.write('\n')

if __name__ == '__main__':
    #getMovieIDFromHTML('Douban_movies_12_28.html', 'id_of_movies.txt')
    #removeDuplicate('id_of_movies.txt', 'distinct_id_of_movies.txt')
    getMovies('distinct_id_of_movies.txt', 'subject_of_movies.txt')
    #getMovieFeatures('subject_of_movies.txt', 'features_of_movies.txt')