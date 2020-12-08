import requests
import time

def downloadFile(name, url, proxies):
    print("downloading {}".format(name))
    r = requests.get(url, proxies=proxies)
    length = float(r.headers['content-length'])
    f = open(name, 'wb')
    count = 0
    count_tmp = 0
    time1 = time.time()
    for chunk in r.iter_content(chunk_size=512):
        if chunk:
            f.write(chunk)
            count += len(chunk)
            if time.time() - time1 > 2:
                p = count / length * 100
                speed = (count - count_tmp) / 1024  / 2
                count_tmp = count
                print(name + ': ' + formatFloat(p) + '%' + ' Speed: ' + formatFloat(speed) + 'KB/S')
                time1 = time.time()
    f.close()


def formatFloat(num):
    return '{:.2f}'.format(num)
    
if __name__ == '__main__':
    
    public_url = "https://storage.googleapis.com/objectron"
    test_lst_name = "book_annotations_test"
    blob_path = public_url + "/v1/index/" + test_lst_name

    proxies = { "http": 'http://127.0.0.1:10809', "https": 'http://127.0.0.1:10809'}

    #video_ids = requests.get(blob_path, proxies=proxies).text
    downloadFile(test_lst_name, blob_path, proxies)

    with open(test_lst_name, 'r') as f:
        video_ids = f.read()
    video_ids = video_ids.split('\n')

    print('Download the first ten videos in book test dataset')

    for i in range(1):
        video_filename = public_url + "/videos/" + video_ids[i] + "/video.MOV"
        metadata_filename = public_url + "/videos/" + video_ids[i] + "/geometry.pbdata"
        annotation_filename = public_url + "/annotations/" + video_ids[i] + ".pbdata"
        
        downloadFile(video_ids[i].replace('/', '_') + "_video.MOV", video_filename, proxies)
        downloadFile(video_ids[i].replace('/', '_') + "_geometry.pbdata", metadata_filename, proxies)
        downloadFile(video_ids[i].replace('/', '_') + ".pbdata", annotation_filename, proxies)
        