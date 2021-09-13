import requests
import time
import datetime
import webbrowser
import httplib2
import emailservice as mail


SCOPES = ['https://www.googleapis.com/auth/gmail.send']
links = {"bb_M28U":"https://www.bestbuy.com/site/gigabyte-28-led-uhd-freesync-monitor-with-hdr-hdmi-displayport-usb-ss-ips-display/6465953.p?skuId=6465953"
         ,"newegg_M28U":"https://www.newegg.com/p/N82E16824012040"
         ,"true_test":"https://www.bestbuy.com/site/lg-27-ultragear-qhd-nano-ips-1ms-165hz-hdr-monitor-with-g-sync-compatibility-black/6451081.p?skuId=6451081"
         }
headers = {"User-Agent":"Mozilla/5.0","cache-control":"max-age=0"} # GET request returns "access denied" if not included
is_sold_out_bb_M28U = False
is_sold_out_newegg_M28U = False
is_sold_out_true_test = False

# Email service setup
email = input("Enter an email to notify (or type skip): ")

def CreateMessage(sender, to, subject, msgPlain):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = to
    msg.attach(MIMEText(msgPlain, 'plain'))
    raw = base64.urlsafe_b64encode(msg.as_bytes())
    raw = raw.decode()
    body = {'raw': raw}
    return body

def SendMessage(sender, to, subject, msgHtml, msgPlain):
    try:
        message = (service.users().messages().send(userId=user_id, body=message).execute())
        print('Message Id: %s' % message['id'])
        return message
    except errors.HttpError as error:
        print('An error occurred: %s' % error)

def check():
    global is_sold_out_bb_FE
    global is_sold_out_bb_M28U
    global is_sold_out_true_test
    global is_sold_out_newegg_M28U

    is_sold_out_bb_M28U = check_single("bb_M28U")
    is_sold_out_newegg_M28U = check_single("newegg_M28U")
    is_sold_out_true_test = check_single("true_test")
    if is_sold_out_true_test:
        print("\x1b[31m" + "Error in code" + "\033[0m")

    print (datetime.datetime.now(),"\nIn stock:\n  bb M28U: ",not is_sold_out_bb_M28U, "\n  newegg M28U: ",not is_sold_out_newegg_M28U)

def check_single(link_url):
    source = requests.get(links[link_url], headers=headers).text
    is_sold_out = (source.__contains__("button class=\"c-button c-button-disabled c-button-lg c-button-block add-to-cart-button\"")
        or source.__contains__("Coming Soon</button></div></div>")
        or source.__contains__("OUT OF STOCK"))
    if not is_sold_out and link_url!="true_test":
        webbrowser.open(links[link_url])
        save_file = open(link_url+".html","w")
        save_file.write(source)
        save_file.close()
        if email!="skip":
            mail.SendMessage("me", email, "M28U in stock", f"M28U is in stock at {links[link_url]}")
    time.sleep(.5)
    return is_sold_out

while True:
    check()
    time.sleep(30)