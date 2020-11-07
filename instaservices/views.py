import threading

import pytz
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.serializers import serialize
from django.db.models import Q
from django.shortcuts import render
from rest_framework.views import APIView
from .task import getProfile, followUserFollowers, userUnFollow, logIn, followUser, unfollowUser, likePost, \
    post_scrapper
from rest_framework.response import Response
from surviral.models import UserAccount, AccountStat, Job, ProfileHistory
import time
import datetime
import random
from django.contrib.auth.models import User


utc = pytz.UTC


class GetProfileAPI(APIView):

    def get_profile_thread(self, username=None, password=None, job_id=None, user_account=None):
        # user_id = self.request.POST.get('useraccount_id')
        # user_account = UserAccount.objects.get(id=user_id)
        response = getProfile.delay(username, password, username, user_account.id)
        while not response.ready():
            print(response.ready(), "posts.ready")
            time.sleep(1)
        # response.get()["driver"].close()
        message = response.get()["posts"]
        print(message)
        if not(message == 'F'):
            try:
                obj = AccountStat.objects.filter(user_account=user_account).last()
                if obj:
                    print(obj.created.date(), " ", datetime.datetime.now().date(), " ",
                          obj.created.date() == datetime.datetime.now().date(), " message = ", message)
                    if obj.created.date() == datetime.datetime.now().date():
                        obj.data = message
                    else:
                        AccountStat.objects.create(user_account=user_account, data=message)
            except:
                AccountStat.objects.create(user_account=user_account, data=message)
            Job.objects.filter(id=job_id).update(status="C")
        else:
            Job.objects.filter(id=job_id).update(status="F")

    def post(self, request, *args, **kwargs):
        # print("inside API\n")
        try:
            username = self.request.POST.get('insta_username')
            password = self.request.POST.get('area_pass')
            a_username = self.request.POST.get('user_a')
            b_username = self.request.POST.get('user_b')
            country_code = self.request.POST.get('area_country')
            # areas = self.request.POST.getlist('checks')
            admin_id =self.request.POST.get('admin_user')
            print(admin_id)
            user = User.objects.get(id=admin_id)
            print(user)

            if user.is_superuser:
                if not username and not password and not country_code:
                    # import pdb;pdb.set_trace()
                    user_id = self.request.POST.get('useraccount_id')
                    user_account = UserAccount.objects.get(id=user_id)
                    if user_account:
                        try:
                            jobs = Job.objects.filter(user_account=user_account)
                            if jobs:
                                for job in jobs:
                                    if job.status=='P':
                                        return Response({"success": True, "previous_task_status": "Pending"})
                            else:
                                pass
                        except Exception as e:
                            pass
                    username = user_account.account_username
                    password = user_account.account_password
                else:

                    user_account = UserAccount.objects.create(user=user, account_type='IG', auth_type="CL",
                                                              account_username=username, account_password=password,
                                                              account_a_username=a_username, account_b_username=b_username,
                                                              data={"country": country_code},
                                                              status='A')
                print(username, password, country_code)
                # else:
                #     user_account = UserAccount.objects.get(user=self.request.user)
                if username:
                    try:
                        # import pdb; pdb.set_trace()
                        # print("Starting Celery Task\n")

                        user_account.login_status = 'IN'
                        user_account.save()

                        job = Job.objects.create(user=self.request.user, user_account=user_account, job_type='GET_PROFILE',
                                           job_title='''Get User's Profile''', app_type='IG',
                                           scheduled_for=datetime.datetime.now(pytz.utc),
                                           status='P')

                        thread = threading.Thread(target=self.get_profile_thread, args=(username, password, job.id, user_account))
                        thread.start()

                        # send email using threading

                        return Response(
                            {"success": True, "profile called": username, "data": ""}
                        )

                    except Exception as e:
                        Job.objects.create(user=user, user_account=user_account, job_type='GET_PROFILE',
                                           job_title='''Get User's Profile''', app_type='IG',
                                           scheduled_for=datetime.datetime.now(pytz.utc),
                                           status='F')
                        return Response(
                            {"success": False, "profile called": username, "Message": str(e)}
                        )
                else:
                    Job.objects.create(user=user, user_account=user_account, job_type='GET_PROFILE',
                                       job_title='''Get User's Profile''', app_type='IG',
                                       scheduled_for=datetime.datetime.now(pytz.utc),
                                       status='F')
                    return Response(
                        {"success": False, "Message": "Profile Name is required but given {}".format(username)}
                    )
            else:
                return Response(
                    {"success": False, "Message": "Not Admin"}
                )
        except Exception as e:
            print(e)
            return Response(
                {"success": False, "Message": "Profile Name is required"}
            )


class FollowUserFollowersAPIv1(APIView):
    def follow_User_Followers_thread(self,username, target_username, password, limit,job_id, user_account_id):
        try:
            response = followUserFollowers.delay(username, target_username, password, int(limit), user_account_id)
            while not response.ready():
                print(response.ready())
                time.sleep(1)

            message = response.get()["message"]
            if message == 'F':
                Job.objects.filter(id=job_id).update(status="F")
            else:
                Job.objects.filter(id=job_id).update(status="C")

            return Response(
                response.get()
            )
        except Exception as e:
            Job.objects.filter(id=job_id).update(status="F")
            return Response(
                {"success": False, "Message": str(e)}
            )

    def post(self, request, *args, **kwargs):
        username = self.request.POST.get('email', None)
        password = self.request.POST.get('password', None)
        target_username = self.request.POST.get('follow_multiple_users')
        limit = self.request.POST.get('number_of_followers', 10)
        admin_id = self.request.POST.get('admin_user_multi_follow')
        user = User.objects.get(id=admin_id)
        # import pdb;pdb.set_trace()

        user_id = self.request.POST.get('user_id')
        user_account = UserAccount.objects.get(id=user_id)

        if not username and not password:
            if user_account:
                try:
                    jobs = Job.objects.filter(user_account=user_account)
                    if jobs:
                        for job in jobs:
                            if job.status == 'P':
                                return Response({"success": True, "previous_task_status": "Pending"})
                    else:
                        pass
                except Exception as e:
                    pass
                username = user_account.account_username
                password = user_account.account_password

        job = Job.objects.create(user=user, user_account=user_account, job_type='MULTI_USER_FOLLOW',
                           job_title='Follow Multiple Users', app_type='IG',
                           scheduled_for=datetime.datetime.now(pytz.utc),
                           status='P')
        thread = threading.Thread(target=self.follow_User_Followers_thread, args=(username, target_username,
                                                                                  password, limit,
                                                                                  job.id, user_account.id))
        thread.start()
        return Response(
            {"success": True}
        )


class UnfollowUserFollowersAPI(APIView):
    def unfollow_threading(self, username, password, limit, job_id, user_account_id):
        response = userUnFollow.delay(username, password, int(limit), user_account_id)
        while not response.ready():
            time.sleep(1)

        message = response.get()["message"]
        if message == 'F':
            Job.objects.filter(id=job_id).update(status="F")
        else:
            Job.objects.filter(id=job_id).update(status="C")

    def post(self, request, *args, **kwargs):
        password = self.request.POST.get('password', None)
        username = self.request.POST.get('email', None)
        limit = self.request.POST.get('number_Unfollower', 20)
        admin_id = self.request.POST.get('admin_user_multi_unfollow')
        user = User.objects.get(id=admin_id)



        user_id = self.request.POST.get('user_id')
        user_account = UserAccount.objects.get(id=user_id)

        if not username and not password:
            if user_account:
                try:
                    jobs = Job.objects.filter(user_account=user_account)
                    if jobs:
                        for job in jobs:
                            if job.status == 'P':
                                return Response({"success": True, "previous_task_status": "Pending"})
                    else:
                        pass
                except Exception as e:
                    pass
                username = user_account.account_username
                password = user_account.account_password

        job = Job.objects.create(user=user, user_account=user_account, job_type='AUTO_UNFOLLOW',
                           job_title='Unfollow Multiple Users', app_type='IG',
                           scheduled_for=datetime.datetime.now(pytz.utc),
                           status='P')
        try:
            thread = threading.Thread(target=self.unfollow_threading, args=(username, password, limit,
                                                                            job.id, user_account.id))
            thread.start()

            return Response(
                {"success": True, "Message": "Process Initiated"}
            )
        except Exception as e:
            Job.objects.filter(id=job.id).update(status="F")
            return Response(
                {"success": False, "Message": str(e)}
            )


class SignInAPI(APIView):
    def get(self, request, *args, **kwargs):
        # import pdb;pdb.set_trace()
        emailId = self.request.GET.get('email', None)
        password = self.request.GET.get('password', None)
        userProfile = self.request.GET.get('userProfile', None)
        if emailId and password:
            try:
                print(emailId, password)
                response = logIn.delay(user_profile=userProfile, email=emailId, password=password)
                while not response.ready():
                    time.sleep(1)
                return Response(
                    response.get()
                )
            except Exception as e:
                return Response(
                    {"success": False, "Message": str(e)}
                )
        else:
            return Response(
                {"success": False, "Message": "Incorrect email: {} or password: {}".format(emailId, password)}
            )


class FollowCandidateAPI(APIView):

    def follow_user_threading(self, target_user, username, password, job_id, user_account_id):
        response = followUser.delay(user_profile=target_user, email=username, password=password, user_account_id=user_account_id)
        while not response.ready():
            time.sleep(1)

        message = response.get()["message"]
        if message == 'F':
            Job.objects.filter(id=job_id).update(status="F")
        else:
            Job.objects.filter(id=job_id).update(status="C")

    def post(self, request, *args, **kwargs):
        target_user = self.request.POST.get('follow_user_name', None)
        username = self.request.POST.get('email', None)
        password = self.request.POST.get('password', None)
        admin_id = self.request.POST.get('admin_user_single_follow')
        user = User.objects.get(id=admin_id)

        user_id = self.request.POST.get('user_id')
        print(user_id, type(user_id), "   sbvgsvbnsgvbnfuivnbfuivbgntgn")
        user_account = UserAccount.objects.get(id=user_id)

        if not username and not password:
            if user_account:
                try:
                    jobs = Job.objects.filter(user_account=user_account)
                    if jobs:
                        for job in jobs:
                            if job.status == 'P':
                                return Response({"success": True, "previous_task_status": "Pending"})
                    else:
                        pass
                except Exception as e:
                    pass
                username = user_account.account_username
                password = user_account.account_password

        job = Job.objects.create(user=user, user_account=user_account, job_type='USERNAME_FOLLOW',
                           job_title='Follow Single User', app_type='IG',
                           scheduled_for=datetime.datetime.now(pytz.utc),
                           status='P')

        if target_user:
            try:
                thread = threading.Thread(target=self.follow_user_threading, args=(target_user, username, password,
                                                                                   job.id, user_account.id))
                thread.start()
                return Response(
                    {"success": True, "Message": "Process Initiated"}
                )
            except Exception as e:
                Job.objects.filter(id=job.id).update(status="F")
                return Response(
                    {"success": False, "Message": str(e)}
                )
        else:
            Job.objects.filter(id=job.id).update(status="F")
            return Response(
                {"success": False, "Message": "Invalid candidate: {}".format(target_user)}
            )


class UnFollowUserAPI(APIView):
    def get(self, request, *args, **kwargs):
        target_user = self.request.GET.get('target_username', None)
        emailId = self.request.GET.get('email', None)
        password = self.request.GET.get('password', None)
        if target_user:
            try:
                response = unfollowUser.delay(user_profile=target_user, email=emailId, password=password)
                while not response.ready():
                    time.sleep(1)
                return Response(
                    response.get()
                )
            except Exception as e:
                return Response(
                    {"success": False, "Message": str(e)}
                )
        else:
            return Response(
                {"success": False, "Message": "Invalid candidate: {}".format(target_user)}
            )


class LoginStatusAPI(APIView):
    def get(self, request, *args, **kwargs):
        print(self.request.GET)
        user_ids = self.request.GET.get('user_id')
        print(user_ids, " Ids")
        user_ids = [int(user_id) for user_id in user_ids.split()]
        print(user_ids)

        try:
            users = UserAccount.objects.filter(Q(id__in=user_ids, login_status='IN') |
                                               Q(id__in=user_ids, login_status='OUT'))
            # print(users, " Users")
            if users:
                data = serialize('json', users)
                return Response({"success": True, "otp_required_user": data})
            return Response({"success": True, "message": "No one required OTP verification"})
        except Exception as e:
            print(str(e))
            return Response({"success": False, "message": "Some error has occured"})


class LikePostsAPI(APIView):

    def like_post_threading(self, username, password, hashtag, user_account_id=1, job_id=None, num_of_likes=None):
        response = likePost.delay(email=username, password=password, user_id=user_account_id, hashtag=hashtag,
                                  limit=int(num_of_likes))
        while not response.ready():
            time.sleep(1)
        message = response.get()["message"]
        if message == 'F':
            Job.objects.filter(id=job_id).update(status="F")
        else:
            Job.objects.filter(id=job_id).update(status="C")
        return Response({"success": True, "Message": "Process Completed {} ".format(response.get()["message"])})

    def post(self, request, *args, **kwargs):
        hashtag = self.request.POST.get('hashtag_name')
        num_of_likes = self.request.POST.get('num_posts_like')
        print(num_of_likes, type(num_of_likes))
        user_id = self.request.POST.get('user_id')
        user_account = UserAccount.objects.get(id=user_id)
        username, password = None, None

        if hashtag and num_of_likes:
            if user_account:
                try:
                    jobs = Job.objects.filter(user_account=user_account)
                    if jobs:
                        for job in jobs:
                            if job.status == 'P':
                                return Response({"success": True, "previous_task_status": "Pending"})
                    else:
                        pass
                except Exception as e:
                    pass
                username = user_account.account_username
                password = user_account.account_password

        job = Job.objects.create(user=self.request.user, user_account=user_account, job_type='LIKE_MULTIPLE_POSTS',
                                 job_title='Like Posts of {} hashtag'.format(hashtag), app_type='IG',
                                 scheduled_for=datetime.datetime.now(pytz.utc),
                                 status='P')

        try:
            thread = threading.Thread(target=self.like_post_threading, args=(username, password, hashtag,
                                                                             user_account.id, job.id, num_of_likes))
            thread.start()
            return Response(
                {"success": True, "Message": "Process Initiated"}
            )
        except Exception as e:
            Job.objects.filter(id=job.id).update(status="F")
            return Response({"Message": str(e)})


class UnFollowSingleUserAPI(APIView):
    pass


class PostScrappingAPI(APIView):

    def post_scrapping_threading(self, target_user, username, password, initial_post_status, user_account_id=1,job_id=None):
        response = post_scrapper.delay(user_profile=target_user, email=username, password=password,
                                       user_id=user_account_id,recent_post=initial_post_status)
        while not response.ready():
            time.sleep(1)

        message = response.get()["message"]
        if message == 'F':
            Job.objects.filter(id=job_id).update(status="F")
        else:
            if response.get()['message'] == 'post filtered and posted back':
                user_account = UserAccount.objects.get(id=user_account_id)
                user_account.initial_post_status = True
                user_account.save()
                Job.objects.filter(id=job_id).update(status="C")
        return Response({"success": True, "Message": "Process Completed {} ".format(response.get())})

    def post(self, request, *args, **kwargs):
        user_id = self.request.POST.get('useraccount_id')
        user_account = UserAccount.objects.get(id=user_id)
        username, password, source_username, initial_post_status = None, None, None, False

        if user_account:
            username = user_account.account_username
            password = user_account.account_password
            source_username = user_account.account_b_username
            initial_post_status = user_account.initial_post_status

        if initial_post_status:
            job = Job.objects.create(user=self.request.user, user_account=user_account, job_type='INSERT_RECENT_POSTS',
                                     job_title='Post latest posts from B account', app_type='IG',
                                     scheduled_for=datetime.datetime.now(pytz.utc),
                                     status='P')
        else:
            job = Job.objects.create(user=self.request.user, user_account=user_account, job_type='INSERT_INITIAL_POSTS',
                                     job_title='Post initial 15 posts in your account', app_type='IG',
                                     scheduled_for=datetime.datetime.now(pytz.utc),
                                     status='P')

        try:
            thread = threading.Thread(target=self.post_scrapping_threading, args=(source_username, username, password,
                                                                                  initial_post_status, user_account.id,
                                                                                  job.id))
            thread.start()
            return Response(
                {"success": True, "Message": "Process Initiated"}
            )
        except Exception as e:
            Job.objects.filter(id=job.id).update(status="F")
            return Response({"Message": str(e)})


class SinglePostAPI(APIView):

    def post(self, request, *args, **kwargs):
        print(self.request.FILES, "\n\n", self.request.POST)
        caption = self.request.POST.get('post_caption')
        image = self.request.FILES.get('selected_image')

        print(image, " ", caption)