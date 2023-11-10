from playwright.sync_api import sync_playwright,Page,expect

import time
import csv

file_path = 'data.csv' #my csv file

#done to write table header
with open(file_path, 'a', newline='') as csvfile:
    csv_writer=csv.writer(csvfile)
    csv_writer.writerow(['Date','Record Number','Record Type','Address','Status','Short Notes'])
        

url="https://aca-oregon.accela.com/LANE_CO/Cap/CapHome.aspx?module=CodeCompliance&TabName=CodeCompliance"


#to write in table
def add_to_csv(data):
    
    with open(file_path, 'a', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(data)





with sync_playwright() as playwright:

    #browser launch
    browser= playwright.chromium.launch(headless=False,channel="msedge",slow_mo=500)


  
    


     #new page
    page=browser.new_page()

    #visit website  or complaint  url
    page.goto(url)

    #select complain  as record type
    select_record_type=page.get_by_label('Record Type:')
    select_record_type.select_option("Complaint")  
    time.sleep(5) #you can see the complaint selected upto 5 sec

    #start date
    date_element= page.wait_for_selector('input#ctl00_PlaceHolderMain_generalSearchForm_txtGSStartDate',state='visible')
    date_element.fill('')
    date_element.fill('01/01/2000')
    time.sleep(3)

    #click search button
    search_element=page.wait_for_selector('a#ctl00_PlaceHolderMain_btnNewSearch')
    search_element.click()
    time.sleep(3)

    #download link
    # download_link=page.get_by_role("link",name="Download results")
    # if download_link:
    #     download_link.click()
    #     browser.close()
    #     print("Yes")
    # else:
        
    #    browser.close()

     


    #next method:
    download_link_by_selector=page.locator("#ctl00_PlaceHolderMain_dgvPermitList_gdvPermitList_gdvPermitListtop4btnExport")
    if download_link_by_selector:
       with page.expect_download() as download_info:
         download_link_by_selector.click()
    download = download_info.value
    download.save_as("./data/" + "download")
    path = download.path()
    print(download.path())
    time.sleep(5000)
        
  
    



   
   
                    
            

   
        

    browser.close()

    


   

