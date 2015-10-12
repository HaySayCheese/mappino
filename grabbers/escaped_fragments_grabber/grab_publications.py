import gzip
import time
import codecs
import requests
from selenium.webdriver import Firefox


driver = Firefox()
max_iterations = 50
iterations = 0
# get published publications ids
response = requests.get('http://127.0.0.1:8000/ajax/api/get_publications')
hash_ids = response.json()['data']
for publication_id in hash_ids:
    iterations += 1

    # restart webdriver if needed
    if iterations > max_iterations:
        iterations = 0
        driver.quit()
        driver = Firefox()
    # get html of publication
    print publication_id[1]
    publication_file = codecs.open('templates/' + str(publication_id[0]) + ':' + publication_id[1] + '.html', 'w', 'utf-8')
    driver.get('http://127.0.0.1:8000/map/#!/1/0/0/' + str(publication_id[0]) + ':' + publication_id[1] + '/?l=50.96647,29.891332&z=14')
    html = driver.page_source
    time.sleep(5)

    # write html to file
    publication_file.write(html)
    publication_file.close()

    # gzip html file
    f_in = open('templates/' + str(publication_id[0]) + ':' + publication_id[1] + '.html', 'rb')
    f_out = gzip.open('templates_gziped/' + str(publication_id[0]) + ':' + publication_id[1] + '.html.gz', 'wb', 9)
    f_out.writelines(f_in)
    f_out.close()
    f_in.close()
driver.quit()
