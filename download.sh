#!/bin/sh
jpype="JPype1-0.6.2-cp27-cp27m-win_amd64.whl"
curl -O "http://www.lfd.uci.edu/~gohlke/pythonlibs/tugh5y6j/$jpype" -H "Accept-Encoding: gzip, deflate, sdch" -H "Accept-Language: ko-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4" -H "Upgrade-Insecure-Requests: 1" -H "User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36" -H "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8" -H "Cache-Control: max-age=0" -H "Connection: keep-alive" --compressed
pip install $jpype
