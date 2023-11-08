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
    browser= playwright.chromium.launch(headless=False,slow_mo=500)

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

    row=[]
    while True: # perform table scraping till the pagination doesnt end
  
        #get table
        table = page.wait_for_selector('table#ctl00_PlaceHolderMain_dgvPermitList_gdvPermitList')
        
        #writing in a csv file
        rows = table.query_selector_all('tr')[3:-2] #first 3 were useless and last 2 were pagination elements so excluded them 
        
        for  item in rows:  #row looping
            cells = item.query_selector_all('td')
            
            current_row=[]  #temp list to append items in row
            for cell_item in cells: #looping over  items inside a row  
                if (len(cell_item.inner_text())>0 ): #the shortnotes was empty most of the cases so this was to check empty cells
                    current_row.append((cell_item.inner_text()).strip())
               
                else:
                    current_row.append("null") #null values for empty cells

            add_to_csv(current_row[1:-1]) # to remove 1st item which is checkbox  that was null and last item  which was being repeated  

            # /////////// if print output is needed
            # print(current_row) 
            
                    
            

        pagination_btn=page.get_by_role('link',name="Next >")
        

        #if the pagination link isnt found i.e. pagination_btn is none,the While loop breaks
        if pagination_btn:
            pagination_btn.click() #traverse to new Page and repeat process below While loop
        else:
            break
        

    browser.close()

    


   

