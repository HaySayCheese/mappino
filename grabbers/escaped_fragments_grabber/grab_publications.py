import gzip
import shutil
import time
import codecs
import os
import requests
from selenium.webdriver import Firefox


if os.path.exists('../../static/escaped_fragments/1/0/0/'):
    print 'Would you like to delete previous parsed files? '
    answer = raw_input('Yes/no: ')
    if answer.lower() == 'yes' or answer.lower() == 'y' or not answer:
        shutil.rmtree('../../static/escaped_fragments/')
        os.mkdir('../../static/escaped_fragments')

else:
    os.makedirs('../../static/escaped_fragments/1/0/0/')


driver = Firefox()
max_iterations = 50
iterations = 0
print 'Parsing is started...'
# get published publications ids
try:
    response = requests.get('http://mappino.com.ua/ajax/api/v1/system/publications/published-ids/')
    hash_ids = response.json()['data']
except:
    print 'API is not working'
    driver.quit()
    exit()


sitemap_file = codecs.open('../../static/publications_sitemap.xml', 'w', 'utf-8')
sitemap_file.write('<?xml version="1.0" encoding="UTF-8"?>\n'
                   '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
for publication_id in hash_ids:
    iterations += 1

    # restart webdriver if needed
    if iterations % max_iterations == 0:
        driver.quit()
        driver = Firefox()
    # get html of publication
    print 'Published publication hash_id = ' + publication_id[1]
    driver.get('http://mappino.com.ua/map/#!/1/0/0/' + str(publication_id[0]) + ':' + publication_id[1] + '/?l=50.96647,29.891332&z=14')
    html = driver.page_source
    time.sleep(3)

    # write url to sitemap
    sitemap_file.write('<url>\n\t<loc>{0}</loc>\n\t<priority>0.8</priority>\n</url>\n'.format(
        'http://mappino.com.ua/map/#!/1/0/0/' + str(publication_id[0]) + ':' + publication_id[1] + '/'))

    # gzip html file
    publication_file = gzip.open('../../static/escaped_fragments/1/0/0/' + str(publication_id[0]) + ':' + publication_id[1] + '.html.gz', 'wb', 9)
    publication_file.writelines(html.encode('utf-8'))
    publication_file.close()
    print 'Created gziped template'


sitemap_file.write('</urlset>')
sitemap_file.close()
driver.quit()
print 'Congratulations! You did it! Parsing is over:3 You parsed ' + str(iterations) + ' templates'