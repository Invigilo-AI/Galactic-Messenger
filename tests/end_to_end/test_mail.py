import pytest

from env import env
from mail import setup_email


@pytest.mark.asyncio
async def test_send_email_plain():
    send_email = setup_email(env.TEST_MAIL_EMAIL, env.TEST_MAIL_PASSWORD)
    assert (
        await send_email(
            {
                "to": env.TEST_MAIL_DESTINATION_EMAIL,
                "subject": "Unit Test Run Successful - Great Job!",
                "message": """
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
            }
        )
        is True
    )


@pytest.mark.asyncio
async def test_send_email_attachment():
    send_email = setup_email(env.TEST_MAIL_EMAIL, env.TEST_MAIL_PASSWORD)
    assert (
        await send_email(
            {
                "to": env.TEST_MAIL_DESTINATION_EMAIL,
                "subject": "Celebrating Our Unit Test Success! 🎉",
                "message": """
Dear Fellow Software Engineer,

I hope this email finds you in high spirits. I am thrilled to announce that our unit tests for the Alert Service have run successfully, marking a significant milestone for our team. As we celebrate this achievement, I wanted to take a moment to express my gratitude and appreciation for your exceptional work.

To commemorate this occasion, I have attached a picture of a majestic seagull soaring across the ocean. Seagulls symbolize freedom, resilience, and adaptability, qualities that resonate with our team's dedication and expertise. Just as these birds navigate the skies with grace, we navigate the complexities of software development, ensuring the stability and reliability of our codebase.

Running effective unit tests is vital to our development process, and your diligent efforts in writing comprehensive tests have greatly contributed to the overall quality of our project. By passing these tests successfully, you have demonstrated your expertise and commitment to delivering high-quality code, enabling us to provide a reliable product to our users.

Your attention to detail and dedication to writing thorough unit tests not only save time and effort in the long run but also prevent potential issues during integration and deployment. Your contributions are invaluable in maintaining the integrity and robustness of our software.

On behalf of the entire team, I comend you for your exceptional performance. Your commitment to excellence reflects positively on our collective efforts, and I am confident that, with your continued dedication, we will achieve even greater milestones in the future.

Should you have any questions, suggestions, or ideas regarding the testing process or any other aspect of our project, please don't hesitate to reach out to me. I am here to support you and provide any assistance you may need.

Once again, congratulations on this significant accomplishment! Let's take a moment to celebrate our success and look forward to the exciting challenges and milestones that lie ahead.

Thank you for your unwavering commitment to excellence.

Best regards,

Akrit Woranithiphong
Your Fellow Software Engineer
Invigilo AI Safety Video Analytics
        """,
                "attachment_name": "segual.png",
                "attachment": open("tests/data/SampleImage.jpg", "rb").read(),
            }
        )
        is True
    )
