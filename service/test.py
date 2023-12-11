# Author - Akshita Patil
import unittest
from unittest.mock import Mock

from data_model_pb2 import Comment, TopCommentsRequest, VoteRequest, VoteAction
from server import RedditServicer, Post


class TestRedditServicer(unittest.TestCase):
    def setUp(self):
        # Set up the test environment
        self.service = RedditServicer()
        self.context = Mock()

    def test_get_post_content_existing_post(self):
        # Mocking the posts dictionary with a sample post
        post_id = "1"
        sample_post = Post(
            post_id=post_id,
            title="Sample Post",
            text="This is a sample post.",
            author="Sample Author"
        )
        self.service.posts = {post_id: sample_post}

        post = self.service.GetPostContent(Post(post_id=post_id), self.context)

        # Asserting that the returned result matches the expected sample post
        self.assertEqual(post, sample_post)

    def test_get_post_content_nonexistent_post(self):
        # Mocking the posts dictionary without the requested post
        post_id = "1"
        self.service.posts = {}  # No posts in this case

        post = self.service.GetPostContent(Post(post_id=post_id), self.context)

        # Asserting that the returned result is None for a non-existent post
        self.assertIsNone(post)

    def test_get_top_comments_existing_post(self):
        # Mocking the posts dictionary with a sample post
        post_id = "1"
        sample_post = Mock(post_id=post_id, title="Sample Post", text="This is a sample post.")
        self.service.posts = {post_id: sample_post}

        # Mocking the comments dictionary with sample comments
        sample_comments = [
            Comment(comment_id="1", text="Comment 1", author="Author 1", score=5, hidden=False),
            Comment(comment_id="2", text="Comment 2", author="Author 2", score=3, hidden=False),
            Comment(comment_id="3", text="Comment 3", author="Author 3", score=7, hidden=False),
        ]
        self.service.comments = {comment.comment_id: comment for comment in sample_comments}

        # Creating a request with the sample post ID and N = 2
        request = TopCommentsRequest(post_id=post_id, N=2)

        # Calling the GetTopComments method
        result_comments = list(self.service.GetTopComments(request, self.context))

        # Asserting that the returned result matches the expected top comments
        self.assertEqual(len(result_comments), 2)
        self.assertEqual(result_comments[0].comment_id, "3")  # Top comment with the highest score
        self.assertEqual(result_comments[1].comment_id, "1")  # Second top comment

    def test_get_top_comments_nonexistent_post(self):
        # Mocking the posts dictionary without the requested post
        post_id = "1"
        self.service.posts = {}  # No posts in this case

        # Creating a request with a non-existent post ID
        request = TopCommentsRequest(post_id=post_id, N=2)

        # Calling the GetTopComments method
        result = list(self.service.GetTopComments(request, self.context))

        # Asserting that the result is an empty list for a non-existent post
        self.assertEqual(result, [])

    def test_expand_comment_branch_existing_comment(self):
        # Mocking the comments dictionary with a sample comment
        comment_id = "1"
        sample_comment = Comment(
            comment_id=comment_id,
            text="Sample Comment",
            author="Sample Author",
            score=5,
            hidden=False,
            publication_date="2023-12-12T12:00:00Z"
        )
        self.service.comments = {comment_id: sample_comment}

        # Creating a request with the sample comment ID and N = 2
        request = TopCommentsRequest(comment_id=comment_id, N=2)

        # Calling the ExpandCommentBranch method
        result_comments = list(self.service.ExpandCommentBranch(request, self.context))

        # Asserting that the returned result matches the expected expanded comment branch
        self.assertEqual(len(result_comments), 3)  # Including the original comment and two child comments
        self.assertEqual(result_comments[0].comment_id, comment_id)  # Original comment
        self.assertEqual(result_comments[1].comment_id, str(len(self.service.comments) + 1))  # First child comment
        self.assertEqual(result_comments[2].comment_id, str(len(self.service.comments) + 2))  # Second child comment

    def test_expand_comment_branch_nonexistent_comment(self):
        # Mocking the comments dictionary without the requested comment
        comment_id = "1"
        self.service.comments = {}  # No comments in this case

        # Creating a request with a non-existent comment ID
        request = TopCommentsRequest(comment_id=comment_id, N=2)

        # Calling the ExpandCommentBranch method
        result = list(self.service.ExpandCommentBranch(request, self.context))

        # Asserting that the result is an empty list for a non-existent comment
        self.assertEqual(result, [])

    def test_vote_comment_existing_comment_upvote(self):
        # Mocking the comments dictionary with a sample comment
        comment_id = "1"
        sample_comment = Comment(
            comment_id=comment_id,
            text="Sample Comment",
            author="Sample Author",
            score=5,
            hidden=False,
            publication_date="2023-12-12T12:00:00Z"
        )
        self.service.comments = {comment_id: sample_comment}

        # Creating a request with the sample comment ID and an upvote action
        request = VoteRequest(comment_id=comment_id, action=VoteAction.UPVOTE)

        # Calling the VoteComment method
        result_comment = self.service.VoteComment(request, self.context)

        # Asserting that the comment score is updated after an upvote
        self.assertEqual(result_comment.score, sample_comment.score + 1)

    def test_vote_comment_existing_comment_downvote(self):
        # Mocking the comments dictionary with a sample comment
        comment_id = "1"
        sample_comment = Comment(
            comment_id=comment_id,
            text="Sample Comment",
            author="Sample Author",
            score=5,
            hidden=False,
            publication_date="2023-12-12T12:00:00Z"
        )
        self.service.comments = {comment_id: sample_comment}

        # Creating a request with the sample comment ID and a downvote action
        request = VoteRequest(comment_id=comment_id, action=VoteAction.DOWNVOTE)

        # Calling the VoteComment method
        result_comment = self.service.VoteComment(request, self.context)

        # Asserting that the comment score is updated after a downvote
        self.assertEqual(result_comment.score, sample_comment.score - 1)

    def test_vote_comment_nonexistent_comment(self):
        # Mocking the comments dictionary without the requested comment
        comment_id = "1"
        self.service.comments = {}  # No comments in this case

        # Creating a request with a non-existent comment ID
        request = VoteRequest(comment_id=comment_id, action=VoteAction.UPVOTE)

        # Calling the VoteComment method
        result = self.service.VoteComment(request, self.context)

        # Asserting that the result is None for a non-existent comment
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
