# Author - Akshita Patil

import grpc
import data_model_pb2_grpc, data_model_pb2


# A client class for interacting with the Reddit gRPC service.

class RedditClient:
    def __init__(self, host='localhost', port=50053):
        """
               Initializes the RedditClient.

               Args:
                   host (str): The hostname or IP address of the gRPC server. Defaults to 'localhost'.
                   port (int): The port number of the gRPC server. Defaults to 50053.
               """
        channel = grpc.insecure_channel(f'{host}:{port}')
        self.stub = data_model_pb2_grpc.RedditServiceStub(channel)

    def create_post(self):
        """
            Create a new post.

            Generates a dummy post object with predefined attributes and sends it to the Reddit service.
            Prints the result, including the created post details.

            """
        post = data_model_pb2.Post(
            title="Dummy Post Title",
            text="This is a dummy post text.",
            video_url="https://example.com/dummy_video.mp4",
            author="Dummy Author",
            score=-1,  # Dummy score (negative)
            state=data_model_pb2.HIDDEN,  # Dummy state (hidden)
            publication_date="2023-12-10T12:00:00Z"  # Dummy publication date (ISO 8601 format)
        )
        result = self.stub.CreatePost(post)
        print(f"\nCreated Post: {result}")

    def vote_post(self):
        """
           Vote on a post.

           Sends a vote request for a dummy post to the Reddit service and prints the result, including the updated post details.

           """
        post_id = "1"  # Dummy post ID
        action = 0  # Dummy vote action (0 for UPVOTE)
        result = self.stub.VotePost(data_model_pb2.VoteRequest(post_id=post_id, action=action))
        print(f"\nVoted Post: {result}")

    def get_post_content(self):
        """
            Retrieve and print the content of a post.

            Sends a request to the Reddit service to get the content of a dummy post and prints the retrieved post content.

            """
        post_id = "1"  # Dummy post ID
        post = self.stub.GetPostContent(data_model_pb2.Post(post_id=str(post_id)))
        print(f"\nRetrieved Post Content:\n{post}")

    def create_comment(self):
        """
            Create a dummy comment and print the result.

            Sends a request to the Reddit service to create a dummy comment and prints the result.

            """
        comment = data_model_pb2.Comment(
            post_id="1",
            text="This is a dummy comment.",
            author="Dummy Author",
            score=0,  # Initialize score for the new comment
            hidden=False,  # New comments are not hidden by default
            publication_date="2023-12-10T12:00:00Z"
        )

        result = self.stub.CreateComment(comment)

        print(f"\nCreated Comment:\n{result}")

    def vote_comment(self):
        """
           Vote on a dummy comment and print the result.

           Sends a request to the Reddit service to vote on a dummy comment (UPVOTE) and prints the result.

           """
        comment_id = "1"  # Dummy post ID
        action = 0  # Dummy vote action (0 for UPVOTE)
        result = self.stub.VoteComment(data_model_pb2.VoteRequest(comment_id=comment_id, action=action))
        print(f"\nVoted Comment: {result}")

    def get_top_comments(self):
        """
            Retrieve and print the top N comments under a dummy post.

            Sends a request to the Reddit service to retrieve the top N comments under a dummy post
            and prints details such as comment ID, score, and whether replies exist.

            """
        post_id = "1"  # Dummy post ID
        N = 5  # Replace with the desired value of N
        top_comments_response = self.stub.GetTopComments(data_model_pb2.TopCommentsRequest(post_id=post_id, N=N))

        print(f"\nTop {N} Comments under Post {post_id}:\n")
        for comment in top_comments_response:
            print(f"Comment ID: {comment.comment_id}, Score: {comment.score}, Replies Exist: {comment.replies_exist}")

    def expand_comment_branch(self):
        """
            Expand and print a comment branch for a dummy comment.

            Sends a request to the Reddit service to expand a comment branch for a dummy comment,
            retrieves and prints details such as comment ID and score for the expanded comments.

            """
        comment_id = "1"  # Dummy comment ID
        N = 5  # Replace with the desired value of N
        expanded_comments = self.stub.ExpandCommentBranch(data_model_pb2.TopCommentsRequest(comment_id=comment_id, N=N))

        print(f"\nExpanded Comment Branch for Comment {comment_id}:\n")
        for expanded_comment in expanded_comments:
            print(
                f"Comment ID: {expanded_comment.comment_id}, Score: {expanded_comment.score}")

    def monitor_updates(self):
        """
            Monitor and print score updates for a post and its comments.

            Initiates a call to the Reddit service with a post ID and a stream of comment IDs,
            then receives and prints updates for the post and its comments.

            """
        post_id = "1"  # Dummy post ID
        comment_ids = ["1", "2", "3"]  # Dummy comment IDs

        # Initiate the call with the post and stream comment IDs
        updates = self.stub.MonitorUpdates(iter(
            [data_model_pb2.UpdateRequest(post_id=post_id)] + [data_model_pb2.UpdateRequest(comment_id=c) for c in
                                                               comment_ids]))

        # Receive and print updates
        for update in updates:
            print(f"Entity ID: {update.entity_id}, Updated Score: {update.score}")


def main():
    client = RedditClient()

    print("Choose an API to call:")
    print("1. Create a Post")
    print("2. Upvote or downvote a Post")
    print("3. Retrieve Post Content")
    print("4. Create a Comment")
    print("5. Upvote or downvote a Comment")
    print("6. Get N most upvoted Comments under a post")
    print("7. Expand Comment branch")
    print("8. Monitor Updates")

    choice = input("Enter the number of your choice: ")

    if choice == "1":
        client.create_post()

    elif choice == "2":
        client.vote_post()

    elif choice == "3":  # Added case for retrieving post content
        client.get_post_content()

    elif choice == "4":  # Added case for creating a comment
        client.create_comment()

    elif choice == "5":
        client.vote_comment()

    elif choice == "6":
        client.get_top_comments()

    elif choice == "7":
        client.expand_comment_branch()

    elif choice == "8":
        client.monitor_updates()

    else:
        print("Invalid choice. Exiting.")


if __name__ == '__main__':
    main()
