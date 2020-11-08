from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome(executable_path="chromedriver.exe")  ## can be firefox or any other browser

# driver.get("https://www.dmcc.ae/business-search?directory=1&submissionGuid=9c0954d2-8d9c-4f94-a10a-276e858db841")
driver.get(
    "https://www.publiccontractsscotland.gov.uk/Search/Search_Auth.aspx?fbclid=IwAR0ZbSAMoavAGI9dcuHHLKUtwFIc6imM936v-K-E8-eX4dbtosTbxT6p2x8")

# creating csv file to upload database
filename = "customerData_publicConstractsScotland.csv"
# opening file
f = open(filename, "w", encoding='utf-8')

# adding header
#f.write("ID, Name, Phone, Email")  ## THERE IS NO ID , you can create easily in excel
f.write( " Name, GeneralEmail, ContactEmail")
f.write("\n")
# waiting 10sec for iframe to load
time.sleep(5)


def GetFromCompany(*ID):

    info= " "
    #driver.get("https://www.publiccontractsscotland.gov.uk/Search/Search_AuthProfile.aspx?ID="+ ID )
    time.sleep(1)
    try:
        driver.find_element_by_xpath('//*[@id="Tab1"]/span/span/span').click()
    except:
        print("It is clicked probably ")
    try:
        comp_name = driver.find_element_by_xpath(
            '//*[@id="ctl00_ContentPlaceHolder1_authority_profile1_lblName"]').get_attribute("innerHTML")
        info += comp_name
        #print(comp_name)
    except:
        comp_name = " "
        info += comp_name
        print("error1 - NO name " )
    info += ","

    try:
        GeneralEmail = driver.find_element_by_xpath(
            '//*[@id="ctl00_ContentPlaceHolder1_authority_profile1_lblEmail"]').get_attribute("innerHTML")
        info += GeneralEmail
        #print(GeneralEmail)
    except:

        GeneralEmail = " "
        info += GeneralEmail
        print("error2 - NO GeneralEmail " )
    info += ","

    ## Goes to contact Details
    driver.find_element_by_xpath('/html/body/form/div[6]/div/div/div/div[3]/div/div/ul/li[2]').click()
    time.sleep(1)
    try: 
        ContactEmail = driver.find_element_by_xpath(
            '//*[@id="ctl00_ContentPlaceHolder1_authority_profile1_lblContactEmail"]').get_attribute("innerHTML") 
        info += ContactEmail
        #print(ContactEmail)
    except:
        ContactEmail = " "
        info += ContactEmail
        print("error3 - NO ContactEmail " )
    info += "\n"
    print(info)
    return info
 
 
def scrapedata(Page):
    time.sleep(1)
    listing=""
    for i in range(1,10+1):
        driver.find_element_by_xpath('//*[@id="ctl00_maincontent_updatePanelMain"]/div/div[2]/div[2]/table/tbody/tr['+str(i)+']/td[1]/a').click()
        driver.switch_to.window(driver.window_handles[1])
        info = GetFromCompany()
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        
        #print(info)

        listing+=info

    #print(listing)

    return listing




try:
    ## name   second div changes
    for i in range(1,162):
        time.sleep(1)
       # print(str(i+1)+ "," + scrapedata())
        print(i)
        f.write(scrapedata(i))
        driver.find_element_by_xpath('//*[@id="ctl00_maincontent_PagingHelperTop_btnNext"]/i').click()


except:
    print("fail")
    # if exception occurs we close our csv file
    f.close()

f.close()