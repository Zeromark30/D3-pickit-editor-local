import os
import json
import requests
import urllib2 
from bs4 import BeautifulSoup
from collections import OrderedDict

# GLOBAL VARIABLES */

BATTLENET_BASEURL = "http://us.battle.net/d3/en/item/"
BATTLENET_APIURL  = "https://us.battle.net/api/d3/data/item/"
BATTLENET_ITEMURL = "http://us.battle.net"

#object to fill items from battle.net
itemArr = []
requestCount = 0
errorCount = 0
itemCount = 0


# FUNCTION DECLARATIONS */

def getBattleNetItems():
    catArr = (
      'helm',
      'spirit-stone',
      'voodoo-mask',
      'wizard-hat',
      'pauldrons',
      'chest-armor',
      'cloak',
      'bracers',
      'gloves',
      'belt',
      'mighty-belt',
      'pants',
      'boots',
      'amulet',
      'ring',
      'shield',
      'crusader-shield',
      'mojo',
      'orb',
      'quiver',
      'enchantress-focus',
      'scoundrel-token',
      'templar-relic',
      'axe-1h',
      'dagger',
      'mace-1h',
      'spear',
      'sword-1h',
      'ceremonial-knife',
      'fist-weapon',
      'flail-1h',
      'mighty-weapon-1h',
      'axe-2h',
      'mace-2h',
      'polearm',
      'staff',
      'sword-2h',
      'daibo',
      'flail-2h',
      'mighty-weapon-2h',
      'bow',
      'crossbow',
      'hand-crossbow',
      'wand',
      'phylactery',
      'scythe-1h',
      'scythe-2h'
    )
    for cat in catArr:
        collectBattleNetItems(cat)
    requestsDone()

def collectBattleNetItems(type):
     url = BATTLENET_BASEURL + type + '/'
     global requestCount 
     requestCount += 1
     res  = requests.get(url)
     body = urllib2.urlopen(url)
     if res.status_code == 200:
        resArr = parseBattleNetItems(body, type)
        itemArr.extend(resArr)
     else :
        errorCount+= 1
        print('ERROR | Status: {}'.format(res.status_code))
# end def collectBattleNetItems


def parseBattleNetItems(body, type):
    #$ = cheerio.load(body) 
    global soup
    soup = BeautifulSoup(body, 'html.parser') 
    resArr = []
    count = 0
    # selector for items with full description
    descSel = soup.select(".legendary .item-details-text a, .set .item-details .item-details-text a")
    # selector for items with description only in the tooltip
    shortSel = soup.select('.data-cell')
    print shortSel
    for itemsdesc in descSel:
      count+= 1
    # end for

    for itemsshort in shortSel:
      count+= 1
    # end for

    if count == 0:
      global errorCount
      errorCount+= 1
      print('ERROR | Status: no Items found')
      return
    # end if
    global requestCount
    print ('START | Type: {} | Request Nr.: {}'.format(type, requestCount))

    for detailSel in descSel:
      item = OrderedDict()
      # selector for the item details
      #print detailSel
      detailSelclass = detailSel.get('class')
      #print toQuality(detailSelclass[0])

      item['item_url'] = BATTLENET_ITEMURL + detailSel.get('href')
      item          = getSharedAttributes(detailSel, item, type)
      item['quality']  = toQuality(detailSelclass[0])
      item['name']     = detailSel.get_text()

      print('--item: ' + item['url_name'])

      resArr.extend([item])
      global itemCount
      itemCount+= 1
    # end for

    for itemsshort in shortSel:
      item      = {}
      item['item_url'] = BATTLENET_ITEMURL + shortSel.get('href')
      item          = getSharedAttributes(shortSel, item, type)

      requestCount+= 1
      print('START | Type: battle.net api | Request Nr.: '+requestCount)
      res  = request.get(item.api_url)
      body = BeautifulSoup(res, 'html.parser')  
      if res.status_code == 200:
        resobj   = JSON.parse(body)
        item.quality = toQuality(resobj.displayColor)
        item.name    = resobj.name
        console.log(chalk.green('--item: ' + item.url_name))
        resArr.extend(item)
        itemCount+= 1
      # end if
      
      else:
        errorCount+= 1
        console.error(chalk.red('ERROR | Status: '+res.statusCode))
    # end for


    print('END | Type: {} | Item Count: {}'.format(type,count))

    return resArr
# end def parseBattleNetItems


#get content who shares the same sub selectors
def getSharedAttributes(context, item, type):
    item['url_name'] = item['item_url'].rsplit('/', 1)[-1]
    item['api_url']  = BATTLENET_APIURL + item['url_name']
    item['type']    = type

    return item

def toQuality(displayColor):
    #print displayColor
    if displayColor=="white":
        return "common"
    elif displayColor=="blue":
        return "magic"
    elif displayColor=="yellow":
        return "rare"
    elif displayColor=="orange":
        return "legendary"
    elif displayColor=="green":
        return "set"
    elif displayColor=="d3-color-default":
        return "common"
    elif displayColor=="d3-color-blue":
        return "magic"
    elif displayColor=="d3-color-yellow":
        return "rare"
    elif displayColor=="d3-color-orange":
        return "legendary"
    elif displayColor=="d3-color-green":
        return "set" 

def requestsDone():
# end def requestsDone
    print ('INFO | Requests {} Items {}'.format(requestCount, itemCount))
    if errorCount > 0:
        print "ERROR | " +errorCount+ " errors occurred"
        print "WARNING | file-saving aborted"
        return
    #print itemArr
    saveFile(itemArr)


def saveFile(data):
    with open('itemlist.json', 'w') as outfile:
        json.dump(data, outfile, indent=2)
    print('INFO | save successful')


if __name__ == "__main__":
    getBattleNetItems()
