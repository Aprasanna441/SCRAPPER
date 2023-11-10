from playwright.sync_api import sync_playwright,Page,expect
import time
import csv

url="https://aca-oregon.accela.com/LANE_CO/Cap/CapHome.aspx?module=CodeCompliance&TabName=CodeCompliance"

class OHLaneScraper:
      
      # method to interact with elements
      def __init__(self):
         self.url=url

      def click_elements(self):
        #select complain  as record type
        select_record_type=self.page.get_by_label('Record Type:')
        select_record_type.select_option("Complaint")  
        time.sleep(5) #you can see the complaint selected upto 5 sec

        #start date
        date_element= self.page.wait_for_selector('input#ctl00_PlaceHolderMain_generalSearchForm_txtGSStartDate',state='visible')
        date_element.fill('')
        date_element.fill('01/01/2000')
        time.sleep(3)

        #click search button
        search_element=self.page.wait_for_selector('a#ctl00_PlaceHolderMain_btnNewSearch')
        search_element.click()
        time.sleep(3)
        self.download()

      #method to visit page
      def visit_page(self):
        with sync_playwright() as playwright:

             #browser launch
            browser = playwright.chromium.launch(headless=False,channel="msedge",slow_mo=500)

            #new page
            self.page=browser.new_page()
            self.page.goto(self.url)

            self.click_elements()
       

            browser.close()

            #visit website  or complaint  url
            
        
      def download(self):
           download_link_by_selector=self.page.locator("#ctl00_PlaceHolderMain_dgvPermitList_gdvPermitList_gdvPermitListtop4btnExport")
           if download_link_by_selector:
            with self.page.expect_download() as download_info:
                download_link_by_selector.click()
            download = download_info.value
            download.save_as("./data/OOP/" + "download")
            path = download.path()
            print(download.path())
            time.sleep(5000)


obj=OHLaneScraper()
obj.visit_page()
obj.click_elements()
obj.download()



                
                    


  



      



