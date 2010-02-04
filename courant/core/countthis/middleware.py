class CountThisMiddleware(object):

    def process_request(self, request):
        """
        This is the very first thing that runs. If it catches a request to /updatecount/
        it updates the count and then returns a blank page, preventing any further
        execution.
        """
        if request.path[0:13] == '/updatecount/':
            #Update the count
            import base64
            decoded = base64.b64decode(request.path[13:-1])
            objects = decoded.split(';')

            from courant.core.countthis.models import do_update_count
            for object in objects:
                parts = object.split('~')
                do_update_count(parts[0], parts[1], parts[2], 'view_count')

            #Return the response
            from django.http import HttpResponse
            return HttpResponse('Counted')
        else:
            return None

    def process_response(self, request, response):
        """
        This checks to see if any countthis requests have been made, and then compiles
        the JavaScript/image bug to make the call to /updatecount/, which is caught by the
        process_request function above.
        """
        if 'countthis' in request.META:
            index = response.content.upper().find('</BODY>')

            if index != -1:
                countthisbug = self.generate_bug(request.META['countthis'])
                response.content = response.content[:index] + countthisbug + response.content[index:]

        return response

    def generate_bug(self, objects):
        import base64
        from time import time

        string = ';'.join(objects)
        string = base64.b64encode(string)

        return """
        <script type="text/javascript" src="%(string)s"></script>
        <noscript><img width="0" height="0" src="%(string)s" /></noscript>
        """ % {'string': '/updatecount/' + string + '/?time=' + str(time())}
