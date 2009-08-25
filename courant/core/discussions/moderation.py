from comment_utils.moderation import CommentModerator
import datetime


class CourantModerator(CommentModerator):

    def comments_open(self, obj):
        if self._get_delta(datetime.datetime.now(), obj.published_at).days >= obj.comment_options.close_after:
            return False
        return True

    def allow(self, comment, content_object):
        # check that anonymous users are allowed
        if not content_object.comment_options.allow_anonymous and not comment.user:
            return False

        # otherwise just return whether or not comments are open
        return self.comments_open(content_object)

    def moderate(self, comment, content_object):
        opts = content_object.comment_options

        # a registered user's post should not be moderated if
        # only moderating anonymous users
        if opts.moderate_anonymous_only and comment.user:
            return False

        # check the time delta to see if that matches the parameters
        if self._get_delta(datetime.datetime.now(), content_object.published_at).days >= opts.moderate_after:
            return True

        # if it didn't match the time limit then let it go public
        return False
