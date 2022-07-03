# utf-8
import requests
from bs4 import BeautifulSoup


def main_soup_from_url(url):
    response = requests.get(url)
    response.encoding = response.apparent_encoding
    main_soup = BeautifulSoup(response.text, 'html.parser')

    return main_soup


def get_urls(original_url, keyword):
    main_soup = main_soup_from_url(original_url)
    urls = []

    a_tag = main_soup.find_all('a')

    for a in a_tag:
        if a.text.find(keyword) > -1:
            url = a.attrs['href']
            if url[:7] != 'http://':
                url = original_url + url
            urls.append(url)

    return urls


def rsplit_characters(text, rsp_chrs):
    for rsp_chr in rsp_chrs:
        text = text.rsplit(rsp_chr)[0]
    return text


def replace_characters(text,rep_chrs):
    for rep_chr in rep_chrs:
        text = text.replace(rep_chr[0],rep_chr[1])
    return text

def delete_characters(text, del_chrs):
    for del_chr in del_chrs:
        text = text.replace(del_chr, '')
    return text


def end_find(text, end_chrs):
    end_n = len(text)

    for end_chr in end_chrs:
        find_n = text.find(end_chr)
        if find_n > -1 and find_n < end_n:
            end_n = find_n

    if end_n < len(text):
        return end_n
    else:
        return -1

def match_characters(aim_chr,mat_chrs):
    for mat_chr in mat_chrs:
        if aim_chr == mat_chr:
            return True
    
    return False

def get_dialogue(url):
    main_soup = main_soup_from_url(url)

    td_tag = main_soup.find_all('td', class_='word')
    if len(td_tag) > 0:
        return get_dialogue_float(main_soup)
    else:
        return get_dialogue_int(main_soup)


def get_dialogue_int(main_soup):
    font_tag = main_soup.find_all('font')

    texts = []
    blank = True

    sep_chr = '：'
    del_chrs = ['\n', '　']
    sta_chrs = ['（']
    fin_chrs = ['）']
    end_chrs = '。！？〜～）'

    for value in font_tag:
        text = delete_characters(value.text, del_chrs)
        name_n = text.find('：')

        if(name_n > -1):
            name = text[:name_n]
            text = text[name_n + 1:]
            end_n = end_find(text, end_chrs)

            while end_n > -1:
                while end_n < len(text) and match_characters(text[end_n], end_chrs):
                    if match_characters(text[end_n], fin_chrs):
                        end_n += 1
                        if match_characters(text[0], sta_chrs):
                            break
                        else:
                            end_n += end_find(text[end_n:], end_chrs)
                    end_n += 1
                
                texts.append(name + sep_chr + text[:end_n])
                text = text[end_n:]
                end_n = end_find(text, end_chrs)

            if len(text) > 0:
                texts.append(name + sep_chr + text)

            blank = False
        elif(not blank):
            texts.append('')
            blank = True

    return texts


def get_dialogue_float(main_soup):
    td_tag = main_soup.find_all('td', class_='word')

    texts = []
    blank = True
    new_sentence = True

    sep_chr = '：'
    rep_chrs = [['\n\n','\t'],['〜','～']]
    del_chrs = ['\n', '\u3000', '\xa0', ' ', '　']
    sta_chrs = ['「','（']
    fin_chrs = ['」','）']
    end_chrs = ['。', '！', '？', '～'] + fin_chrs

    for value in td_tag:
        text = value.text
        text = replace_characters(text, rep_chrs)
        text = delete_characters(text, del_chrs)

        if end_find(text,sta_chrs) > -1:
            end_n = end_find(text, end_chrs)

            while end_n > -1:
                name_n = end_find(text, sta_chrs)

                if (name_n > -1 and name_n < end_find(text, end_chrs)) or new_sentence:
                    name = text[:name_n]
                    
                    if name[0] == '\t':
                        texts.append('')
                        name = name.replace('\t','')
                    
                    text = text[name_n + 1:]
                    end_n = end_find(text, end_chrs)
                    new_sentence = False

                while match_characters(text[end_n], end_chrs):
                    if match_characters(text[end_n],fin_chrs):
                        new_sentence = True

                        if match_characters(text[end_n - 1], end_chrs):
                            text = text.replace(text[end_n], '', 1)
                        else:
                            text = text.replace(text[end_n], '。', 1)
                            end_n += 1
                        
                        break
                        
                    end_n += 1

                texts.append(name + sep_chr + text[:end_n])
                text = text[end_n:]
                end_n = end_find(text, end_chrs)

            if len(text) > 0:
                texts.append(name + sep_chr + text)

            blank = False
        if(not blank):
            texts.append('')
            blank = True

    return texts


url = 'http://radical-d.extrem.ne.jp/'
urls = get_urls(url, '霊夢')

for i in range(len(urls)):
    texts = get_dialogue(urls[i])

    with open('reimu_dialogue_' + str(i) + '.txt', 'w') as file:
        for text in texts:
            file.write(text + '\n')
