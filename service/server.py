# Author - Akshita Patil

import grpc
from concurrent import futures
from data_model_pb2 import User, Post, Comment, Subreddit, VoteRequest, VoteAction, UpdateResponse
from data_model_pb2_grpc import RedditServiceServicer, add_RedditServiceServicer_to_server

# Dummy storage in memory
posts = {}
comments = {}

"""
    Implementation of the Reddit gRPC service.

    This class provides server-side implementation for the Reddit API service
    using gRPC. It includes methods to create posts, vote on posts/comments,
    retrieve post content, create comments, vote on comments, retrieve top comments,
    expand comment branches, and monitor updates.
    """

class RedditServicer(RedditServiceServicer):
    def CreatePost(self, request, context):
        """
           Creates a new post.

           This method generates a new post ID, stores the post in the 'posts' dictionary,
           and returns the created post.

           Args:
               request: An instance of the Post message containing post details.
               context: The gRPC context.

           Returns:
               Post: The created post.

           Note:
               This implementation is a dummy version and stores posts in memory.
           """
        post_id = str(len(posts) + 1)
        posts[post_id] = request
        return posts[post_id]

    def VotePost(self, request, context):
        """
            Votes on a post (Upvote or Downvote).

            This method retrieves the post with the specified post ID from the 'posts' dictionary,
            increments or decrements the post score based on the vote action, and returns the
            updated post.

            Args:
                request: An instance of the VoteRequest message containing vote details.
                context: The gRPC context.

            Returns:
                Post: The updated post after voting.

            Note:
                This implementation is a dummy version and stores posts in memory.
            """
        post_id = request.post_id  # Convert post_id to int
        post = posts.get(post_id)

        if post:
            if request.action == VoteAction.UPVOTE:
                post.score += 1
            elif request.action == VoteAction.DOWNVOTE:
                post.score -= 1
            return post

    # Implement other service methods similarly
    def GetPostContent(self, request, context):
        """
            Retrieves the content of a post.

            This method retrieves the post with the specified post ID from the 'posts' dictionary
            and returns the post content.

            Args:
                request: An instance of the Post message containing the post ID.
                context: The gRPC context.

            Returns:
                Post: The content of the requested post.

            Note:
                This implementation is a dummy version and retrieves posts from memory.
            """
        post_id = request.post_id  # Convert post_id to int
        post = posts.get(post_id)
        return post

    def CreateComment(self, request, context):
        """
           Creates a new comment.

           This method generates a new comment ID, stores the comment in the 'comments' dictionary,
           and returns the created comment.

           Args:
               request: An instance of the Comment message containing comment details.
               context: The gRPC context.

           Returns:
               Comment: The created comment.

           Note:
               This implementation is a dummy version and stores comments in memory.
           """
        # Dummy implementation - just store in memory
        comment_id = str(len(comments) + 1)
        comments[comment_id] = request
        return comments[comment_id]

    def VoteComment(self, request, context):
        """
            Handles voting on a comment.

            This method retrieves the comment with the specified comment ID from the 'comments' dictionary
            and updates its score based on the provided vote action.

            Args:
                request: An instance of the VoteRequest message containing comment ID and vote action.
                context: The gRPC context.

            Returns:
                Comment: The updated comment.

            Note:
                This implementation is a dummy version and updates comment scores in memory.
            """
        comment_id = request.comment_id  # Convert post_id to int
        comment = comments.get(comment_id)

        if comment:
            if request.action == VoteAction.UPVOTE:
                comment.score += 1
            elif request.action == VoteAction.DOWNVOTE:
                comment.score -= 1
            return comment

    def GetTopComments(self, request, context):
        """
            Retrieves the top comments under a post.

            This method retrieves the post with the specified post ID from the 'posts' dictionary,
            sorts the comments by score in descending order, and returns the top N comments.

            Args:
                request: An instance of the TopCommentsRequest message containing post ID and the number of top comments.
                context: The gRPC context.

            Yields:
                Comment: The top comments under the post.

            Note:
                This implementation is a dummy version and retrieves top comments from memory.
            """
        post_id = request.post_id  # Convert post_id to int
        post = posts.get(post_id)

        if post:
            # Sort comments by score in descending order
            sorted_comments = sorted(comments.values(), key=lambda c: c.score, reverse=True)

            # Get the top N comments
            N = request.N
            top_comments = sorted_comments[:N]

            # Add the replies_exist field to the comments and return the result
            result_comments = []
            for comment in top_comments:
                comment_with_replies = Comment(
                    comment_id="1",
                    text=comment.text,
                    author=comment.author,
                    score=comment.score,
                    hidden=comment.hidden,
                    publication_date=comment.publication_date,
                    replies_exist=False
                )
                result_comments.append(comment_with_replies)

                # Send responses to the client
            for comment in result_comments:
                yield comment
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Post not found")
            return Comment()

    def ExpandCommentBranch(self, request, context):
        """
            Expands a comment branch to show child comments.

            This method retrieves the comment with the specified comment ID from the 'comments' dictionary,
            adds some dummy child comments for testing purposes, and sends the expanded comment branch to the client.

            Args:
                request: An instance of the TopCommentsRequest message containing comment ID and the number of child comments.
                context: The gRPC context.

            Yields:
                Comment: The expanded comment branch, including child comments.

            Note:
                This implementation is a dummy version and adds child comments to the expanded branch in memory.
            """
        comment_id = "1"  # Convert comment_id to int
        comment = comments.get(comment_id)

        print(comment)

        if comment:
            # Add some dummy child comments for testing when expanding a comment branch
            child_comment_id_1 = len(comments) + 1
            child_comment_1 = Comment(
                comment_id=str(child_comment_id_1),
                text="This is a child comment 1.",
                author="Child Author 1",
                score=1,
                hidden=False,
                publication_date="2023-12-12T12:00:00Z"
            )

            child_comment_id_2 = len(comments) + 2
            child_comment_2 = Comment(
                comment_id=str(child_comment_id_2),
                text="This is a child comment 2.",
                author="Child Author 2",
                score=2,
                hidden=False,
                publication_date="2023-12-12T12:00:00Z"
            )

            # Store child comments in memory
            comments[child_comment_id_1] = child_comment_1
            comments[child_comment_id_2] = child_comment_2

            # Send the expanded comment branch to the client
            result_comments = [comment, child_comment_1, child_comment_2]
            for comment in result_comments:
                yield comment
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Comment not found")
            return Comment()

    # Extra Credit
    def MonitorUpdates(self, request, context):
        """
            Monitors updates for the post and its comments.
    
            This method initializes scores for the post and its comments, sends initial scores to the client,
            and processes additional comment IDs from the client stream, sending corresponding score updates.
    
            Args:
                request: An instance of the UpdateRequest message containing the post ID.
                context: The gRPC context.
    
            Yields:
                UpdateResponse: The score updates for the post and its comments.
    
            Raises:
                grpc.RpcError: If there is an issue with the client stream.
    
            Note:
                This implementation uses an asynchronous client stream to handle updates from the client.
            """
        # Initialize scores for the post and its comments
        post_id = request.post_id
        post = posts.get(post_id)
        if post:
            self.current_scores[post_id] = post.score
            for comment_id in post.comments:
                comment = comments.get(comment_id)
                if comment:
                    self.current_scores[comment_id] = comment.score
    
            # Send initial scores to the client
            yield self.create_update_response(post_id, self.current_scores[post_id])
            for comment_id in post.comments:
                yield self.create_update_response(comment_id, self.current_scores[comment_id])
    
            # Process additional comment IDs from the client stream
            try:
                async for comment_id in context.stream:
                    comment = comments.get(comment_id)
                    if comment:
                        self.current_scores[comment_id] = comment.score
                        yield self.create_update_response(comment_id, self.current_scores[comment_id])
                    else:
                        context.set_code(grpc.StatusCode.NOT_FOUND)
                        context.set_details(f"Comment with ID {comment_id} not found")
            except grpc.RpcError as e:
                # Handle client stream termination (e.g., when the client stops sending comment IDs)
                if e.code() == grpc.StatusCode.CANCELLED:
                    print("Client stream terminated")
                else:
                    raise
    
    def create_update_response(self, entity_id, score):
        return UpdateResponse(entity_id=entity_id, score=score)


def serve():
    """
        Start the gRPC server to serve the Reddit service.

        This function initializes the gRPC server, adds the RedditServicer, and starts
        listening on a specified port.
        """
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_RedditServiceServicer_to_server(RedditServicer(), server)
    server.add_insecure_port('[::]:50053')  # Use your desired port

    print("Server started. Listening on port 50053...")
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
