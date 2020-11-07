import datetime
import glob
import os
import random
import re
import shutil
import time

import pyautogui
import pytz
import requests
from selenium import webdriver
from selenium.webdriver.support import ui
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import imaplib
import email as webmail
from selenium.webdriver.support.wait import WebDriverWait
from insta_web_bot.celery import app as celery_app
from surviral.models import UserAccount
from django.conf import settings
utc=pytz.UTC

BASE_DIR = settings.BASE_DIR

DRIVER_PATH = settings.DRIVER_PATH

# DRIVE_PATH = '/usr/bin/chromedriver'
#ENVIRONMENT = "Local"

def browser_profile(email):
    browserProfile = webdriver.ChromeOptions()
    browserProfile.add_argument("--start-maximized")
    browserProfile.add_argument('user-data-dir=user_profiles/'+email)

    browserProfile.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
    # browserProfile.add_experimental_option("detach", True)
    return browserProfile

@celery_app.task(bind=True)
def getProfile(self, emailInput, passwordInput, target_name, user_id):
    message = {}

    print("Inside Celery Task\n")
    print(DRIVER_PATH)
    driver = webdriver.Chrome(DRIVER_PATH , options=browser_profile(target_name))

    driver.get('https://www.instagram.com/'+target_name)
    time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
    try:
        try:
            login_button=None
            try:
                #login_button = driver.find_element_by_xpath("/html/body/div/div[1]/header/div/div[3]/ul/li/a/strong")
                login_button = driver.find_element_by_xpath('//strong[text() = "Log In"]')
            except Exception as e:
                print(str(e))
                #login_button=driver.find_element_by_xpath("/html/body/div[1]/section/nav/div[2]/div/div/div[3]/div/span/a[1]/button")
                login_button = driver.find_element_by_xpath('//button[text() = "Log In"]')
            finally:
                if login_button:
                    print("check login button 1")
                    login_button.click()
                    time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
                    # print("1")
                    driver=signIn(driver,emailInput,passwordInput, user_id)
                    time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
                    try:
                        notification_button = driver.find_element_by_xpath('//button[text() = "Not Now"]')
                        time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
                        notification_button.click()
                        time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
                    except Exception as e:
                        print(str(e))
                        pass

                    try:
                        if not driver.find_element_by_class_name('k9GMp'):
                            search_button = driver.find_element_by_xpath('//input[@placeholder="Search"]')
                            search_button.send_keys(emailInput)
                            time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
                            profile_button = driver.find_element_by_xpath('//span[text() = "{}"]'.format(emailInput))
                            time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
                            profile_button.click()
                            time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
                    except Exception as e:
                        print(str(e))
                        pass
        except Exception as e:
            print(str(e))
            print("check login button 2")
            driver=otpSignIn(driver, emailInput, passwordInput, user_id)
            time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
            try:
                notification_button = driver.find_element_by_xpath('//button[text() = "Not Now"]')
                time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
                notification_button.click()
                time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
            except Exception as e:
                print(str(e))
                pass

            try:
                if not driver.find_element_by_class_name('k9GMp'):
                    search_button = driver.find_element_by_xpath('//input[@placeholder="Search"]')
                    search_button.send_keys(emailInput)
                    time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
                    profile_button = driver.find_element_by_xpath('//span[text() = "{}"]'.format(emailInput))
                    time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
                    profile_button.click()
                    time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
            except Exception as e:
                print(str(e))
                pass
    except Exception as e:
        print(str(e))
        pass
    finally:
        time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
        # print("5")
        try:
            response = driver.find_element_by_class_name('k9GMp')
        except:
            driver.close()
            return {'posts': 'F'}
        else:
            for i in response.text.split('\n'):
                val, key = i.split()
                message[key] = int(val)
            time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
            driver.close()
            return {"posts":message}



@celery_app.task(bind=True)
def followUserFollowers(self,email,target_username,password,follow_limit=20, user_account_id=None):
    driver = webdriver.Chrome(DRIVER_PATH , options=browser_profile(email))
    actionChain = webdriver.ActionChains(driver)
    driver.get('https://www.instagram.com/' + target_username + '/')
    time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
    try:
        try:
            login_button = None
            try:
                # login_button = driver.find_element_by_xpath("/html/body/div/div[1]/header/div/div[3]/ul/li/a/strong")
                login_button = driver.find_element_by_xpath('//strong[text() = "Log In"]')
            except Exception as e:
                print(str(e))
                # login_button=driver.find_element_by_xpath("/html/body/div[1]/section/nav/div[2]/div/div/div[3]/div/span/a[1]/button")
                login_button = driver.find_element_by_xpath('//button[text() = "Log In"]')
            finally:
                if login_button:
                    print("check login button 1")
                    login_button.click()
                    time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
                    # print("1")
                    driver = signIn(driver, email, password, user_account_id)
                    time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
                    try:
                        notification_button = driver.find_element_by_xpath('//button[text() = "Not Now"]')
                        time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
                        notification_button.click()
                        time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
                    except Exception as e:
                        print(str(e))
                        pass

                    try:
                        if not driver.find_element_by_xpath("//a[contains(@href,'followers')]"):
                            search_button = driver.find_element_by_xpath('//input[@placeholder="Search"]')
                            search_button.send_keys(target_username)
                            time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
                            profile_button = driver.find_element_by_xpath(
                                '//span[text() = "{}"]'.format(target_username))
                            time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
                            profile_button.click()
                            time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
                    except Exception as e:
                        print(str(e))
                        pass

        except Exception as e:
            print(str(e))
            print("check login button 2")
            driver = otpSignIn(driver, email, password, user_account_id)
            time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
            try:
                notification_button = driver.find_element_by_xpath('//button[text() = "Not Now"]')
                time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
                notification_button.click()
                time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
            except Exception as e:
                print(str(e))
                pass

            try:
                if not driver.find_element_by_xpath("//a[contains(@href,'followers')]"):
                    search_button = driver.find_element_by_xpath('//input[@placeholder="Search"]')
                    search_button.send_keys(target_username)
                    time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
                    profile_button = driver.find_element_by_xpath('//span[text() = "{}"]'.format(target_username))
                    time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
                    profile_button.click()
                    time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
            except Exception as e:
                print(str(e))
                pass
    except Exception as e:
        pass
    finally:
        try:
            j = 1
            print(follow_limit, "follow limit")
            for _ in range(follow_limit//10 +1):
                if (j<=follow_limit):
                    followers=driver.find_element_by_xpath("//a[contains(@href,'followers')]")
                    time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
                    try:
                        followers.click()
                        time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
                        i=1
                        xpath = "/html/body/div[4]/div/div/div[2]/ul/div/li[%d]/div/div[3]/button"%int(i)
                        while xpath:

                            #j=j+1
                            if i > 10:
                                close_button = driver.find_element_by_xpath("/html/body/div[4]/div/div/div[1]/div/div[2]/button")
                                time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
                                close_button.click()
                                time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
                                driver.get(driver.current_url)
                                break

                            if not j<=(follow_limit):
                                print("Limit reached")
                                driver.close()
                                return {"status": True, "message": "limit reached"}

                            followers_elems = driver.find_elements_by_xpath(xpath)
                            try:
                                if followers_elems[0].text=="Follow":
                                    followers_elems[0].click()

                                    time.sleep(get_random_wait(initial_limit=10, upper_limit=15))
                                    followers_elems = driver.find_elements_by_xpath(xpath)
                                    time.sleep(get_random_wait(initial_limit=5, upper_limit=8))
                                    if followers_elems[0].text == "Requested":
                                        time.sleep(get_random_wait(initial_limit=1, upper_limit=5))
                                        followers_elems[0].click()
                                        time.sleep(get_random_wait(initial_limit=1, upper_limit=5))
                                        unfollow = driver.find_element_by_xpath(
                                            '//button[normalize-space()="Unfollow"]')
                                        unfollow.click()
                                        time.sleep(get_random_wait(initial_limit=1, upper_limit=5))
                                        #follow_limit += 1
                                        xpath = "/html/body/div[4]/div/div/div[2]/ul/div/li[%d]/div/div[3]/button" % int(
                                            i + 1)
                                    else:
                                        xpath = "/html/body/div[4]/div/div/div[2]/ul/div/li[%d]/div/div[3]/button" % int(
                                            i + 1)
                                    i+=1
                                    j = j + 1

                                    time.sleep(get_random_wait(initial_limit=20, upper_limit=30))

                                elif followers_elems[0].text=="Following":
                                    xpath = "/html/body/div[4]/div/div/div[2]/ul/div/li[%d]/div/div[3]/button" % int(i + 1)
                                    i += 1
                                    j = j + 1
                                    #follow_limit += 1
                                    time.sleep(get_random_wait(initial_limit=4, upper_limit=8))

                                elif followers_elems[0].text=="Requested":
                                    xpath = "/html/body/div[4]/div/div/div[2]/ul/div/li[%d]/div/div[3]/button" % int(i + 1)
                                    i += 1
                                    j = j + 1
                                    #follow_limit += 1
                                    time.sleep(get_random_wait(initial_limit=4, upper_limit=8))
                                else:
                                    i+=1
                                    j = j + 1
                                    #follow_limit += 1
                                    time.sleep(get_random_wait(initial_limit=2, upper_limit=5))

                            except Exception as e:
                                driver.close()
                                return {"status":False,"message":"F"}

                    except Exception as e:
                        driver.close()
                        return {"status":False,"message":"F"}
                else:
                    print("limit reached")
                    driver.close()
                    return {"status":True,"message":"limit reached"}
        except Exception as e:
            print(str(e))
            driver.close()
            return {"status": False, "message": "F"}






# def refresh_unfollow_elements(driver, user_profile, unfollow_limit, task_type='following'):
#     # is_self True will unfollow own followings, False will follow target following
#     driver.get('https://www.instagram.com/' + user_profile + '/')
#     time.sleep(1)
#     main_element = task_type
#     if task_type == 'unfollow':
#         main_element = 'following'
#     followers = EC.visibility_of_element_located(
#         (By.XPATH, "//a[contains(@href,'"+main_element+"')]")
#         )(driver)
#     time.sleep(1)
#     followers.click()
#     time.sleep(1)
#     if task_type == 'unfollow':
#         unfollow_list =driver.find_elements_by_xpath('//button[normalize-space()="Following"]')[:unfollow_limit]
#     else:
#         unfollow_list =driver.find_elements_by_xpath('//button[normalize-space()="Follow"]')[:unfollow_limit]
#     total_unfollowed = 0
#     for ele_ in unfollow_list:
#         try:
#             if ele_.text=="Following":
#                 ele_.click()
#                 unfollow = driver.find_element_by_xpath('//button[normalize-space()="Unfollow"]')
#                 time.sleep(get_random_wait())
#                 unfollow.click()
#                 # followers_elems[0].send_keys(Keys.ARROW_DOWN)
#                 total_unfollowed += 1
#                 time.sleep(get_random_wait())
#                 print("unfollowed %i so far" % (total_unfollowed))
#                 continue
#             if ele_.text=="Follow":
#                 ele_.click()
#                 total_unfollowed += 1
#                 time.sleep(get_random_wait())
#                 print("followed %i so far" % (total_unfollowed))
#                 continue
#         except Exception as e:
#             print(str(e))
#
#     return total_unfollowed
#

# @celery_app.task(bind=True)
# def userUnFollow(self, user_profile, unfollow_limit=10):
#         driver = webdriver.Chrome(DRIVE_PATH , options=browser_profile(user_profile))
#         total_unfollowed = 0
#         try:
#             while total_unfollowed < unfollow_limit:
#                 total_unfollowed += refresh_unfollow_elements(driver, user_profile, unfollow_limit - total_unfollowed, 'unfollow')
#                 print("total unfollowed ", total_unfollowed)
#                 if total_unfollowed >= unfollow_limit:
#                     break
#         except Exception as e:
#             print(str(e))
#         driver.close()


# @celery_app.task(bind=True)
# def followUserFollowers(self, user_profile,target_username, follow_limit=10, follow_following=False):
#
#     task_type = 'followers'
#     if follow_following:
#         task_type  = 'following'
#     print(task_type)
#     driver = webdriver.Chrome(DRIVE_PATH , options=browser_profile(user_profile))
#     total_followed = 0
#     try:
#         while total_followed < follow_limit:
#             total_followed += refresh_unfollow_elements(driver, target_username, follow_limit - total_followed, task_type)
#             print("total followed ", total_followed)
#             if total_followed >= follow_limit:
#                 break
#     except Exception as e:
#         print(str(e))
#     driver.close()

@celery_app.task(bind=True)
def userUnFollow(self, email, password,unfollow_limit=15, user_account_id=None):
        driver = webdriver.Chrome(DRIVER_PATH , options=browser_profile(email))
        driver.get('https://www.instagram.com/' + email + '/')
        time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
        try:
            try:
                login_button = None
                try:
                    # login_button = driver.find_element_by_xpath("/html/body/div/div[1]/header/div/div[3]/ul/li/a/strong")
                    login_button = driver.find_element_by_xpath('//strong[text() = "Log In"]')
                except Exception as e:
                    print(str(e))
                    # login_button=driver.find_element_by_xpath("/html/body/div[1]/section/nav/div[2]/div/div/div[3]/div/span/a[1]/button")
                    login_button = driver.find_element_by_xpath('//button[text() = "Log In"]')
                finally:
                    if login_button:
                        print("check login button 1")
                        login_button.click()
                        time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
                        # print("1")
                        driver = signIn(driver, email, password, user_account_id)
                        time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
                        try:
                            notification_button = driver.find_element_by_xpath('//button[text() = "Not Now"]')
                            time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
                            notification_button.click()
                            time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
                        except Exception as e:
                            print(str(e))
                            pass

                        try:
                            if not driver.find_element_by_xpath("//a[contains(@href,'following')]"):
                                search_button = driver.find_element_by_xpath('//input[@placeholder="Search"]')
                                search_button.send_keys(email)
                                time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
                                profile_button = driver.find_element_by_xpath('//span[text() = "{}"]'.format(email))
                                time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
                                profile_button.click()
                                time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
                        except Exception as e:
                            print(str(e))
                            pass

            except Exception as e:
                print(str(e))
                print("check login button 2")
                driver = otpSignIn(driver, email, password, user_account_id)
                time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
                try:
                    notification_button = driver.find_element_by_xpath('//button[text() = "Not Now"]')
                    time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
                    notification_button.click()
                    time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
                except Exception as e:
                    print(str(e))
                    pass

                try:
                    if not driver.find_element_by_xpath("//a[contains(@href,'following')]"):
                        search_button = driver.find_element_by_xpath('//input[@placeholder="Search"]')
                        search_button.send_keys(email)
                        time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
                        profile_button = driver.find_element_by_xpath('//span[text() = "{}"]'.format(email))
                        time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
                        profile_button.click()
                        time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
                except Exception as e:
                    print(str(e))
                    pass
        except Exception as e:
            pass
        finally:
            try:
                j=1
                print(unfollow_limit)
                for _ in range((unfollow_limit//10) +1):

                    if j<=unfollow_limit:
                        followers = driver.find_element_by_xpath("//a[contains(@href,'following')]")
                        time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
                        try:
                            followers.click()
                            time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
                            i=1
                            xpath = "/html/body/div[4]/div/div/div[2]/ul/div/li[%d]/div/div[3]/button"%int(i)
                            while xpath:
                                #j = j + 1
                                if i > 10:
                                    close_button = driver.find_element_by_xpath(
                                        "/html/body/div[4]/div/div/div[1]/div/div[2]/button")
                                    time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
                                    close_button.click()
                                    time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
                                    driver.get(driver.current_url)
                                    break

                                if not j<=(unfollow_limit):
                                    time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
                                    print("Limit reached")
                                    driver.close()
                                    return {"status": True, "message": "limit reached"}

                                followers_elems = driver.find_elements_by_xpath(xpath)
                                try:
                                    if followers_elems[0].text=="Follow":
                                        xpath = "/html/body/div[4]/div/div/div[2]/ul/div/li[%d]/div/div[3]/button" % int(i+1)
                                        i+=1
                                        j = j + 1
                                        time.sleep(get_random_wait(initial_limit=2, upper_limit=5))

                                    elif followers_elems[0].text=="Following":
                                        followers_elems[0].click()
                                        time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
                                        xpath = "/html/body/div[4]/div/div/div[2]/ul/div/li[%d]/div/div[3]/button" % int(i + 1)
                                        unfollow = driver.find_element_by_xpath('//button[normalize-space()="Unfollow"]')
                                        unfollow.click()
                                        i += 1
                                        j = j + 1
                                        time.sleep(get_random_wait(initial_limit=20, upper_limit=30))

                                    elif followers_elems[0].text=="Requested":
                                        xpath = "/html/body/div[4]/div/div/div[2]/ul/div/li[%d]/div/div[3]/button" % int(i + 1)
                                        i += 1
                                        j = j + 1
                                        time.sleep(get_random_wait(initial_limit=4, upper_limit=8))

                                except Exception as e:
                                    driver.close()
                                    return {"status":False,"message":"F"}
                        except Exception as e:
                            driver.close()
                            return {"status":False,"message":"F"}
                    else:
                        driver.close()
                        return {"status": True, "message": "limit reached"}
            except Exception as e:
                print(str(e))
                driver.close()
                return {"status": False, "message": "F"}


@celery_app.task(bind=True)
def logIn(self,user_profile,email,password):
    driver = webdriver.Chrome(DRIVER_PATH, options=browser_profile(user_profile))
    driver.get('https://www.instagram.com/'+user_profile)
    time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
    try:
        try:
            login_button=None
            try:
                # login_button = driver.find_element_by_xpath("/html/body/div/div[1]/header/div/div[3]/ul/li/a/strong")
                login_button = driver.find_element_by_xpath('//strong[text() = "Log In"]')
            except:
                # login_button = driver.find_element_by_xpath("/html/body/div[1]/section/nav/div[2]/div/div/div[3]/div/span/a[1]/button")
                login_button = driver.find_element_by_xpath('//button[text() = "Log In"]')
            finally:
                if login_button:
                    login_button.click()
                    time.sleep(2)
                    print("1")
                    driver=signIn(driver,email,password)
                    time.sleep(2)
                    driver.close()
                    return {"status": True, "message": "Logged in"}
        except:
            driver=otpSignIn(driver, email, password)
            time.sleep(2)
            driver.close()
            return {"status": True, "message": "Logged in"}

    except:
        driver.close()
        return {"status": True, "message": "You are Already Logged in"}


@celery_app.task(bind=True)
def followUser(self,user_profile,email,password, user_account_id):
    driver = webdriver.Chrome(DRIVER_PATH, options=browser_profile(email))
    driver.get('https://www.instagram.com/'+user_profile)
    time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
    try:
        try:
            login_button = None
            try:
                # login_button = driver.find_element_by_xpath("/html/body/div/div[1]/header/div/div[3]/ul/li/a/strong")
                login_button = driver.find_element_by_xpath('//strong[text() = "Log In"]')
            except Exception as e:
                print(str(e))
                # login_button=driver.find_element_by_xpath("/html/body/div[1]/section/nav/div[2]/div/div/div[3]/div/span/a[1]/button")
                login_button = driver.find_element_by_xpath('//button[text() = "Log In"]')
            finally:
                if login_button:
                    print("check login button 1")
                    login_button.click()
                    time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
                    # print("1")
                    driver = signIn(driver, email, password, user_account_id)
                    time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
                    try:
                        notification_button = driver.find_element_by_xpath('//button[text() = "Not Now"]')
                        time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
                        notification_button.click()
                        time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
                    except Exception as e:
                        print(str(e))
                        pass


                    try:
                        followButton = driver.find_element_by_css_selector('button')
                        if not (followButton.text == 'Follow'):
                            search_button = driver.find_element_by_xpath('//input[@placeholder="Search"]')
                            search_button.send_keys(user_profile)
                            time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
                            profile_button = driver.find_element_by_xpath('//span[text() = "{}"]'.format(user_profile))
                            time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
                            profile_button.click()
                            time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
                    except Exception as e:
                        print(str(e))
                        pass

        except Exception as e:
            print(str(e))
            print("check login button 2")
            driver = otpSignIn(driver, email, password, user_account_id)
            time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
            try:
                notification_button = driver.find_element_by_xpath('//button[text() = "Not Now"]')
                time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
                notification_button.click()
                time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
            except Exception as e:
                print(str(e))
                pass

            try:
                followButton = driver.find_element_by_css_selector('button')
                if not (followButton.text == 'Follow'):
                    search_button = driver.find_element_by_xpath('//input[@placeholder="Search"]')
                    search_button.send_keys(user_profile)
                    time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
                    profile_button = driver.find_element_by_xpath('//span[text() = "{}"]'.format(user_profile))
                    time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
                    profile_button.click()
                    time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
            except Exception as e:
                print(str(e))
                pass
    except Exception as e:
        print(str(e))
        pass
    finally:
        try:
            followButton = driver.find_element_by_css_selector('button')
            if (followButton.text == 'Follow'):
                time.sleep(get_random_wait(initial_limit=10, upper_limit=15))
                followButton.click()
                time.sleep(get_random_wait(initial_limit=10, upper_limit=15))
                driver.close()
                return {"success": True,"message":"Started Following {}".format(user_profile)}
            else:
                print("You are already following this user")
                driver.close()
                return {"success": True,"message":"You are already following {}".format(user_profile)}
        except Exception as e:
            print(str(e))
            driver.close()
            return {"success": False, "message": "F"}



@celery_app.task(bind=True)
def unfollowUser(self,user_profile,email,password):
    driver = webdriver.Chrome(DRIVER_PATH, options=browser_profile(email))
    driver.get('https://www.instagram.com/'+user_profile)
    time.sleep(2)
    try:
        try:
            login_button = None
            try:
                # login_button = driver.find_element_by_xpath("/html/body/div/div[1]/header/div/div[3]/ul/li/a/strong")
                login_button = driver.find_element_by_xpath('//strong[text() = "Log In"]')
            except Exception as e:
                print(str(e))
                # login_button=driver.find_element_by_xpath("/html/body/div[1]/section/nav/div[2]/div/div/div[3]/div/span/a[1]/button")
                login_button = driver.find_element_by_xpath('//button[text() = "Log In"]')
            finally:
                if login_button:
                    print("check login button 1")
                    login_button.click()
                    time.sleep(2)
                    print("1")
                    driver = signIn(driver, email, password)
                    time.sleep(2)
                    try:
                        notification_button = driver.find_element_by_xpath('//button[text() = "Not Now"]')
                        time.sleep(2)
                        notification_button.click()
                        time.sleep(1)
                    except Exception as e:
                        print(str(e))
                        pass

                    try:
                        search_button = driver.find_element_by_xpath('//input[@placeholder="Search"]')
                        search_button.send_keys(email)
                        time.sleep(2)
                        profile_button = driver.find_element_by_xpath('//span[text() = "{}"]'.format(user_profile))
                        time.sleep(2)
                        profile_button.click()
                        time.sleep(1)
                    except Exception as e:
                        print(str(e))
                        pass

        except Exception as e:
            print(str(e))
            print("check login button 2")
            driver = otpSignIn(driver, email, password)
            time.sleep(2)
            try:
                notification_button = driver.find_element_by_xpath('//button[text() = "Not Now"]')
                time.sleep(2)
                notification_button.click()
                time.sleep(1)
            except Exception as e:
                print(str(e))
                pass

            try:
                search_button = driver.find_element_by_xpath('//input[@placeholder="Search"]')
                search_button.send_keys(email)
                time.sleep(2)
                profile_button = driver.find_element_by_xpath('//span[text() = "{}"]'.format(user_profile))
                time.sleep(2)
                profile_button.click()
                time.sleep(1)
            except Exception as e:
                print(str(e))
                pass
    except Exception as e:
        pass
    finally:
        buttons = driver.find_elements_by_css_selector('button')
        if buttons[0].text=="Message":
            followButton = buttons[1]
            followButton.click()
            time.sleep(1)
            confirmButton = driver.find_element_by_xpath('//button[text() = "Unfollow"]')
            confirmButton.click()
            return {"success": True,"message":"Stopped Following {}".format(user_profile)}
        else:
            print("You are not following this user")
            driver.close()
            return {"success": True,"message":"You are not following {}".format(user_profile)}


def signIn(browser,email,password, user_id):
    print("sign in start")
    time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
    emailInput = browser.find_elements_by_name('username')[0]
    passwordInput = browser.find_elements_by_name('password')[0]
    emailInput.send_keys(email)
    time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
    passwordInput.send_keys(password)
    time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
    passwordInput.send_keys(Keys.ENTER)
    print("sign in completed")
    time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
    try:
        # print("2")
        #saveProfile = browser.find_elements_by_xpath("/html/body/div[1]/section/main/div/div/div/section/div/button")
        saveProfile = browser.find_element_by_xpath('//button[text() = "Save Info"]')
        print(saveProfile,"save profile")
        time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
        saveProfile.click()
        time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
    except:
        pass
    try:
        # print("3")
        #send_otp = browser.find_element_by_xpath("/html/body/div[1]/section/div/div/div[3]/form/span/button")
        send_otp = browser.find_element_by_xpath('//button[text() = "Send Security Code"]')
        time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
        send_otp.click()
        time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
        query = UserAccount.objects.get(id=user_id)
        query.login_status = 'O'
        query.save()
    except:
        pass
    try:
        query = UserAccount.objects.get(id=user_id)
        query.login_status = 'O'
        query.save()
        time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
        # print("4")
        #fill_otp = browser.find_element_by_xpath("/html/body/div[1]/section/div/div/div[2]/form/div/input")
        fill_otp = browser.find_element_by_xpath('//input[@name="security_code"]')
        while True:
            try:
                otp = getOTP(browser, user_id)
                if otp:
                    print(otp, " ", int(otp))
                    time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
                    break
            except:
                time.sleep(get_random_wait(initial_limit=4, upper_limit=6))
        fill_otp.send_keys(int(otp))
        time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
        #submit_otp = browser.find_element_by_xpath("/html/body/div[1]/section/div/div/div[2]/form/span/button")
        submit_otp = browser.find_element_by_xpath('//button[text() = "Submit"]')
        time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
        submit_otp.click()
        time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
    except:
        pass

    return browser


def otpSignIn(driver,email,password, user_id):
    print("inside otpSignIn")
    #login_button = driver.find_element_by_xpath("/html/body/div[1]/section/main/div/article/div/div[1]/div/form/div/div[3]/button")
    login_button = driver.find_element_by_xpath('//button//div[text() = "Log In"]')
    # print(login_button,"ii a mmmmmm here")
    if login_button:
        print("sign in start")
        time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
        emailInput = driver.find_elements_by_name('username')[0]
        passwordInput = driver.find_elements_by_name('password')[0]
        emailInput.send_keys(email)
        time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
        passwordInput.send_keys(password)
        time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
        passwordInput.send_keys(Keys.ENTER)
        print("sign in completed")
        time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
        try:
            # print("2")
            #saveProfile = driver.find_elements_by_xpath("/html/body/div[1]/section/main/div/div/div/section/div/button")
            saveProfile = driver.find_element_by_xpath('//button[text() = "Save Info"]')
            print(saveProfile, "save profile")
            time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
            saveProfile.click()
            time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
        except Exception as e:
            print(e)
            pass
        time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
        try:
            #send_otp = driver.find_element_by_xpath("/html/body/div[1]/section/div/div/div[3]/form/span/button")
            send_otp = driver.find_element_by_xpath('//button[text() = "Send Security Code"]')
            # print(send_otp, "aaaaaaaaaa")
            time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
            send_otp.click()
            time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
            query = UserAccount.objects.get(id=user_id)
            query.login_status = 'O'
            query.save()
        except Exception as e:
            print(e)
            pass
        try:
            query = UserAccount.objects.get(id=user_id)
            query.login_status = 'O'
            query.save()
            time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
            #fill_otp = driver.find_element_by_xpath("/html/body/div[1]/section/div/div/div[2]/form/div/input")
            print("inside fill otp")
            fill_otp = driver.find_element_by_xpath('//input[@name="security_code"]')
            while True:
                try:
                    otp=getOTP(driver, user_id)
                    if otp:
                        print(otp, " ", int(otp))
                        time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
                        break
                except:
                    time.sleep(get_random_wait(initial_limit=4, upper_limit=6))
            fill_otp.send_keys(int(otp))
            time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
            #submit_otp = driver.find_element_by_xpath("/html/body/div[1]/section/div/div/div[2]/form/span/button")
            submit_otp = driver.find_element_by_xpath('//button[text() = "Submit"]')
            time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
            submit_otp.click()
            time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
        except Exception as e:
            print(e)
            pass
        return driver


# def getOTP():
#     body = None
#
#     username = 'geshan919@gmail.com'
#     password = 'used@121987'
#
#     otp = []
#     imap = imaplib.IMAP4_SSL("imap.gmail.com")
#     imap.login(username, password)
#     status, messages = imap.select("Inbox")
#     # number of top emails to fetch
#     N = 1
#     # total number of emails
#     messages = int(messages[0])
#     for i in range(messages, messages - N, -1):
#         res, msg = imap.fetch(str(i), "(RFC822)")
#         for response in msg:
#             if isinstance(response, tuple):
#                 msg = webmail.message_from_bytes(response[1])
#                 body = msg.get_payload(decode=True).decode()
#                 body = body.split('If this was you, please use the following code to confirm your identity:')[1]
#                 body = body.split('''If this wasn't you, please reset your password to secure your account.''')[0]
#                 otp.append(int(body))
#
#     return otp[0]


def getOTP(driver, user_id):
    query = UserAccount.objects.get(id=user_id)
    otp = query.data['otp']
    # driver.execute_script("var a = prompt('Enter OTP', 'OTP');document.body.setAttribute('data-id', a)")
    # time.sleep(30)
    # otp=driver.find_element_by_tag_name('body').get_attribute('data-id')
    # print(int(otp), "OTP ####################################################################")
    return int(otp)


@celery_app.task(bind=True)
def likePost(self,email, password, user_id,hashtag,limit):
    driver = webdriver.Chrome(DRIVER_PATH, options=browser_profile(email))
    driver.get('https://www.instagram.com/'+email)
    try:
        try:
            login_button = None
            try:
                # login_button = driver.find_element_by_xpath("/html/body/div/div[1]/header/div/div[3]/ul/li/a/strong")
                login_button = driver.find_element_by_xpath('//strong[text() = "Log In"]')
            except Exception as e:
                print(str(e))
                # login_button=driver.find_element_by_xpath("/html/body/div[1]/section/nav/div[2]/div/div/div[3]/div/span/a[1]/button")
                login_button = driver.find_element_by_xpath('//button[text() = "Log In"]')
            finally:
                if login_button:
                    print("check login button 1")
                    login_button.click()
                    time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
                    # print("1")
                    driver = signIn(driver, email, password, user_id)
                    time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
                    try:
                        notification_button = driver.find_element_by_xpath("//button[text() = 'Not Now']")
                        time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
                        notification_button.click()
                        time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
                    except Exception as e:
                        print(str(e))
                        pass
                    try:
                        if not driver.find_element_by_class_name('k9GMp'):
                            search_button = driver.find_element_by_xpath("//input[@placeholder='Search']")
                            search_button.send_keys(email)
                            time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
                            profile_button = driver.find_element_by_xpath(
                                '//span[text() = "{}"]'.format(email))
                            time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
                            profile_button.click()
                            time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
                    except Exception as e:
                        print(str(e))
                        pass
        except Exception as e:
            print(str(e))
            print("check login button 2")
            driver = otpSignIn(driver, email, password, user_id)
            time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
            try:
                notification_button = driver.find_element_by_xpath("//button[text() = 'Not Now']")
                time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
                notification_button.click()
                time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
            except Exception as e:
                print(str(e))
                pass
            try:
                if not driver.find_element_by_class_name('k9GMp'):
                    search_button = driver.find_element_by_xpath('//input[@placeholder="Search"]')
                    search_button.send_keys(email)
                    time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
                    profile_button = driver.find_element_by_xpath('//span[text() = "{}"]'.format(email))
                    time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
                    profile_button.click()
                    time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
            except Exception as e:
                print(str(e))
                pass
    except Exception as e:
        print(str(e))
        pass
    finally:
        try:
            like_count = 0
            search_button = driver.find_element_by_xpath("//input[@placeholder='Search']")
            search_button.send_keys(hashtag)
            time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
            profile_button = driver.find_element_by_xpath(
                '//span[text() = "{}"]'.format(hashtag))
            time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
            profile_button.click()
            time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
            while True:
                images = driver.find_elements_by_xpath("//div[@class = 'v1Nh3 kIKUG  _bz0w']")
                print(len(images),"posts length hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhgg")
                try:
                    for div in images:
                        time.sleep(get_random_wait(initial_limit=4, upper_limit=8))
                        div.click()
                        time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
                        like_button = driver.find_elements_by_xpath("//span[@class = 'fr66n']")
                        like_button=like_button[0].find_elements_by_css_selector("[aria-label='Like']")
                        if like_button:
                            time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
                            like_button[0].click()
                            like_count=like_count+1
                            print(like_count)
                            time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
                            webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
                            time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
                            print(like_count, " ", limit, " ", like_count>=limit)
                            if like_count>=limit:
                                break
                        else:
                            time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
                            webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
                            time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
                            continue
                    if like_count == limit:
                        break
                except Exception as e:
                    print(str(e))
                    driver.get('https://www.instagram.com/')
                    time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
                    search_button = driver.find_element_by_xpath("//input[@placeholder='Search']")
                    search_button.send_keys(hashtag)
                    time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
                    profile_button = driver.find_element_by_xpath(
                        '//span[text() = "{}"]'.format(hashtag))
                    time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
                    profile_button.click()
                    time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
                    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
                    time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
                    continue
            print(like_count)
            driver.close()
            return {"status": False,"message": ": Liked {} posts".format(limit)}
        except Exception as e:
            print(str(e))
            driver.close()
            return {"status": False,"message": "F"}


def browser_profile_mobile(email):
    mobile_emulation = {"deviceName": "Nexus 5"}
    browserProfile = webdriver.ChromeOptions()
    browserProfile.add_argument("--start-maximized")
    browserProfile.add_argument('user-data-dir=user_profiles/'+email)

    browserProfile.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
    browserProfile.add_experimental_option("mobileEmulation", mobile_emulation)

    return browserProfile


def autoPost(email,path_list):
    driver = webdriver.Chrome(DRIVER_PATH, options=browser_profile_mobile(email))
    driver.get('https://www.instagram.com/' + email)
    try:
        for name in path_list:
            time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
            button = driver.find_elements_by_css_selector('[aria-label="New Post"]')
            print(button, "Post button")
            button[0].click()
            time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
            pyautogui.hotkey('ctrl', 'l')
            time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
            print("pressed hotkey")
            pyautogui.write(name)
            time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
            pyautogui.press('enter')
            time.sleep(get_random_wait(initial_limit=18, upper_limit=22))
            button = driver.find_elements_by_xpath("//*[contains(text(), 'Next')]")
            print(button)
            button[0].click()
            time.sleep(get_random_wait(initial_limit=8, upper_limit=12))
            field = driver.find_elements_by_tag_name('textarea')[0]
            field.click()
            field.send_keys("#music, #python")
            time.sleep(get_random_wait(initial_limit=12, upper_limit=16))
            button = driver.find_elements_by_xpath("//button[text() = 'Share']")
            print(button, "share button found")
            button[0].click()
            time.sleep(get_random_wait(initial_limit=12, upper_limit=16))
            try:
                button = driver.find_elements_by_xpath("//button[text() = 'Cancel']")
                time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
                button[0].click()
                time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
                continue
            except Exception as e:
                print(str(e))
                pass
            try:
                button = driver.find_elements_by_xpath("//button[text() = 'Not Now']")
                time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
                button[0].click()
                time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
                continue
            except:
                try:
                    driver.find_elements_by_css_selector('[aria-label="New Post"]')
                    continue
                except:
                    os.chdir(BASE_DIR)
                    time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
                    driver = webdriver.Chrome(DRIVER_PATH, options=browser_profile_mobile(email))
                    driver.get('https://www.instagram.com/' + email)
                    time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
                    continue
        driver.close()
    except Exception as e:
        print(e)
        driver.close()


def imageList(driver,user,image_folder,images_unique_extended,limit,image_alt,i,recent_post):
    time.sleep(get_random_wait(initial_limit=4, upper_limit=8))
    images = driver.find_elements_by_xpath("//div[@class = 'v1Nh3 kIKUG  _bz0w']")
    images_url = driver.find_elements_by_xpath("//div[@class = 'v1Nh3 kIKUG  _bz0w']/a/div/div/img[@class ='FFVAD']")
    time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
    images_unique_extended,limit,image_alt,i=filterPost(driver,images,images_url,image_folder,images_unique_extended,limit,image_alt,i,recent_post)
    return images_unique_extended,limit,image_alt,i


def filterPost(driver,images_unique,image_url,image_folder,images_unique_extended,limit,image_alt,i,recent_post):
    mon_dic = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6, "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10,
               "Nov": 11, "Dec": 12}
    for div,img in zip(images_unique,image_url):
        if image_alt and img.get_attribute("alt") in image_alt:
            continue
        time.sleep(get_random_wait(initial_limit=4, upper_limit=8))
        div.click()
        time.sleep(get_random_wait(initial_limit=4, upper_limit=8))
        images_time = driver.find_elements_by_xpath("//time")
        post_date=images_time[0].get_attribute("title")
        date = re.split(' |, ', post_date)
        month = mon_dic[date[0][0:3]]
        day = int(date[1])
        year = int(date[2])
        post_date = utc.localize(datetime.datetime(year=year, month=month, day=day))
        #print(post_date,"postdate after conversion",datetime.datetime(year=year, month=month, day=day),"before conversion")
        image_alt.append(img.get_attribute("alt"))
        times_now=date_as_per_timezone(date_time=datetime.datetime.today(), country="India")
        if not recent_post:
            if post_date < (times_now - datetime.timedelta(days=60)):
                limit = True
                break
            elif post_date<(times_now-datetime.timedelta(days=30)):
                i = i + 1
                time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
                images = img.get_attribute("src")
                path=image_folder+"/"+"image"+str(i)+".jpg"
                with open(path, 'wb') as handler:
                    print(path)
                    img_data = requests.get(images).content
                    handler.write(img_data)
                    images_unique_extended.append(path)
                time.sleep(get_random_wait(initial_limit=4, upper_limit=8))
        elif recent_post:
            print(times_now - datetime.timedelta(days=1),post_date,times_now,sep='\n')
            if post_date < (times_now - datetime.timedelta(hours=24)):
                limit = True
                break
            elif post_date>=(times_now-datetime.timedelta(hours=24)):
                i = i + 1
                time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
                images = img.get_attribute("src")
                path=image_folder+"/"+"image"+str(i)+".jpg"
                with open(path, 'wb') as handler:
                    print(path)
                    img_data = requests.get(images).content
                    handler.write(img_data)
                    images_unique_extended.append(path)
                time.sleep(get_random_wait(initial_limit=4, upper_limit=8))
        webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
        time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
        if len(images_unique_extended) >= 15:
            break
    return images_unique_extended,limit,image_alt,i


@celery_app.task(bind=True)
def post_scrapper(self,user_profile,email,password,user_id,recent_post=False):
    # BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
    print(BASE_DIR, " base_dir")
    if not os.path.isdir(os.path.join(str(BASE_DIR),user_profile)):
        os.chdir(str(BASE_DIR))
        os.mkdir("{}".format(user_profile))
        image_folder=os.path.join(str(BASE_DIR),user_profile)
    else:
        image_folder=os.path.join(str(BASE_DIR),user_profile)
    driver = webdriver.Chrome(DRIVER_PATH, options=browser_profile(email))
    driver.get('https://www.instagram.com/' + user_profile)
    try:
        try:
            login_button = None
            try:
                # login_button = driver.find_element_by_xpath("/html/body/div/div[1]/header/div/div[3]/ul/li/a/strong")
                login_button = driver.find_element_by_xpath('//strong[text() = "Log In"]')
            except Exception as e:
                print(str(e))
                # login_button=driver.find_element_by_xpath("/html/body/div[1]/section/nav/div[2]/div/div/div[3]/div/span/a[1]/button")
                login_button = driver.find_element_by_xpath('//button[text() = "Log In"]')
            finally:
                if login_button:
                    print("check login button 1")
                    login_button.click()
                    time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
                    # print("1")
                    driver = signIn(driver, email, password, user_id)
                    time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
                    try:
                        notification_button = driver.find_element_by_xpath('//button[text() = "Not Now"]')
                        time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
                        notification_button.click()
                        time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
                    except Exception as e:
                        print(str(e))
                        pass
                    try:
                        if not driver.find_element_by_class_name('k9GMp'):
                            search_button = driver.find_element_by_xpath('//input[@placeholder="Search"]')
                            search_button.send_keys(email)
                            time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
                            profile_button = driver.find_element_by_xpath(
                                '//span[text() = "{}"]'.format(email))
                            time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
                            profile_button.click()
                            time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
                    except Exception as e:
                        print(str(e))
                        pass
        except Exception as e:
            print(str(e))
            print("check login button 2")
            driver = otpSignIn(driver, email, password, user_id)
            time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
            try:
                notification_button = driver.find_element_by_xpath('//button[text() = "Not Now"]')
                time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
                notification_button.click()
                time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
            except Exception as e:
                print(str(e))
                pass
            try:
                if not driver.find_element_by_class_name('k9GMp'):
                    search_button = driver.find_element_by_xpath('//input[@placeholder="Search"]')
                    search_button.send_keys(email)
                    time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
                    profile_button = driver.find_element_by_xpath('//span[text() = "{}"]'.format(email))
                    time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
                    profile_button.click()
                    time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
            except Exception as e:
                print(str(e))
                pass
    except Exception as e:
        print(str(e))
        pass
    finally:
        try:
            time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
            images_unique_extended = []
            limit=False
            i=0
            image_alt=[]
            while True:
                images_unique_extended,limit,image_alt,i=imageList(driver,user_profile,image_folder,images_unique_extended,limit,image_alt,i,recent_post)
                driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
                time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
                print(limit,len(images_unique_extended))
                if len(images_unique_extended)>=15:
                    break
                elif limit:
                    break
            driver.close()
            time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
            os.chdir(image_folder)
            path_list = [os.path.join(image_folder, i) for i in glob.glob('*.jpg')]
            time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
            os.chdir(BASE_DIR)
            time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
            if path_list:
                autoPost(email,path_list)
                time.sleep(get_random_wait(initial_limit=2, upper_limit=5))
                if os.path.exists(image_folder) and os.path.isdir(image_folder):
                    shutil.rmtree(image_folder)
                return {"message": "post filtered and posted back"}
            else:
                if os.path.exists(image_folder) and os.path.isdir(image_folder):
                    shutil.rmtree(image_folder)
                return {"message": "No Post Found"}
        except Exception as e:
            print(str(e))
            driver.close()
            return {"status": False, "message": "F"}


def date_as_per_timezone(date_time, country):
    # now = dt.now(pytz.utc)
    tz = [v[0] for k, v in pytz.country_timezones.items() if pytz.country_names[k] == str(country)][0]
    return date_time.astimezone(pytz.timezone(tz))


def get_random_wait(initial_limit=1, upper_limit=5):
    return random.randint(initial_limit, upper_limit)