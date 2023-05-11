from env import env


from mail import (
    set_email,
)


def test_send_email():
    send_email = set_email(env.TEST_EMAIL, env.TEST_PASSWORD)
    assert (
        send_email(
            env.TEST_DESTINATION_EMAIL,
            "Unit Test Run Successful - Great Job!",
            """
Dear Fellow Software Engineer,

I hope this email finds you well. I am pleased to inform you that the unit tests for Alert Service ran successfully! Congratulations to you and the entire team on this achievement.

Running unit tests is an essential part of our development process, ensuring the stability and reliability of our codebase. Your dedication and attention to detail in writing effective unit tests have contributed significantly to the overall quality of our project.

By successfully passing these tests, you have demonstrated your expertise and commitment to producing high-quality code. Your efforts are vital in maintaining the integrity and robustness of our software, and they greatly enhance our ability to deliver a reliable product to our users.

I want to express my gratitude for your hard work and comend you on your exceptional performance. Your diligence in conducting thorough unit testing not only saves time and effort in the long run but also helps prevent potential issues from arising during integration and deployment.

Your dedication to quality reflects positively on our team, and I encourage you to keep up the excellent work. Your contributions are invaluable, and I am confident that with your continued efforts, we will achieve even greater milestones in the future.

Once again, congratulations on this accomplishment, and please feel free to reach out to me if you have any questions or suggestions regarding the testing process or any other aspect of our project. I am always here to support you and provide any assistance you may need.

Thank you for your hard work and commitment to excellence.

Best regards,

Akrit Woranithiphong
Your Fellow Software Engineer
Invigilo AI Safety Video Analytics
        """,
        )
        is True
    )
