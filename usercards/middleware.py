from testforcups.usercards.models import MiddlewareData


class Middleware(object):
    """ Middleware Object"""

    def process_request(self, request):
        """ Handler to store http request"""

        req = MiddlewareData()

        if request.user.is_anonymous():
            req.user = None
        else:
            req.user = request.user
        if 'LANG' in request.META:
            req.lang = request.META['LANG']
        else:
            req.lang = ''

        req.method = request.method
        req.uri = request.build_absolute_uri()
        req.user_agent = request.META['HTTP_USER_AGENT']
        req.uri = request.build_absolute_uri()
        req.addr = request.META['REMOTE_ADDR']
        req.save()