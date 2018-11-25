#!/usr/bin/env python3
import sys,re,urllib.parse
import urllib.request
import string,random
import fileinput
import subprocess
import base64

def main(file_name):
    latex_dict = {}
    f = open(file_name, "r")
    markdown = f.read()
    latexes = re.findall(r'[\$]{1,2}.*?[\$]{1,2}', markdown)
    n = 1
    pathname = base64.b64encode(file_name.encode()).decode('ascii')
    for latex in latexes:
        local_latex_png = download_png(latex, "latex_" + str(n))
        upload_png(local_latex_png, pathname)
        latex_dict[latex] = get_latex_markdown("latex_" + str(n) + ".png", pathname)
        markdown = markdown.replace(latex, latex_dict[latex])
        n = n + 1
    print(latex_dict)
    with open('output.md', 'w') as file:
        file.write(markdown)

def get_latex_markdown(latex_png_file, pathname):
    pic_site_url = "http://dalaoli-shuxue-wx.oss-cn-beijing.aliyuncs.com/"
    png_markdown_text = "![](" + pic_site_url + pathname + "/" + latex_png_file + ")"
    return png_markdown_text

def upload_png(filename, pathname):
    aliyun_bucket = "oss://dalaoli-shuxue-wx/"
    cmd = ["/usr/local/bin/ossutilmac64", "cp",
        "output_png/" + filename,  aliyun_bucket + pathname + "/", "-f"]
    upload_result = subprocess.run(cmd, check=False)
    if upload_result.returncode != 0:
        print("uploading failed for file: " + filename)
    else:
        print("successfully uploading file: " + filename)


def download_png(latex, filename):
    pic_site_url = "http://tex.s2cms.ru/png/"
    pic_download_url = pic_site_url + urllib.parse.quote_plus(latex)
    print("downloading: " + pic_download_url)
    urllib.request.urlretrieve(pic_download_url,
            './output_png/' + filename + '.png')
    return filename + '.png'

if __name__ == "__main__":
    main(sys.argv[1])
