from backend_server.app import db
from backend_server.run import app
from backend_server.app.models import NewsPost

news_data = [
    {
        "title": "Filling Your Mental Health Toolbox With Dr. Rachel Goldman",
        "title_ru": "Пополните Свой Набор Инструментов для укрепления Психического Здоровья с помощью доктора Рэйчел Голдман",
        "description": "Psychologist Rachel Goldman emphasizes the importance of affordable self-care, including quality sleep, physical activity, and stress management.",
        "description_ru": "Психолог Рэйчел Голдман подчеркивает важность доступного ухода за собой, включая качественный сон, физическую активность и управление стрессом.",
        "image_url": "https://www.verywellmind.com/thmb/I2aZTc6DKmyd1oHHuCNF8VhHWRQ=/750x0/filters:no_upscale():max_bytes(150000):strip_icc():format(webp)/Mental-health-lessons-learned-during-COVID-19-no-logo-2d7dcc09105648f19500257244acbbb0.png",
        "url": "https://www.verywellmind.com/filling-your-mental-health-toolbox-with-dr-rachel-goldman-5199795?"
    },
    {
        "title": "Techniques to Reduce Stress and Anxiety",
        "title_ru": "Методы снижения стресса и тревожности",
        "description": "Stress reduction techniques such as breathing exercises, meditation, physical activity, and art therapy improve well-being.",
        "description_ru": "Методы снижения стресса, такие как дыхательные упражнения, медитация, физическая активность и арт-терапия, улучшают самочувствие.",
        "image_url": "https://www.verywellhealth.com/thmb/kHSp-GgMNwAKLRCvARzdIYe_Rjo=/750x0/filters:no_upscale():max_bytes(150000):strip_icc():format(webp)/how-to-reduce-stress-5207327_FINAL-907db114a640431ba1e8ecbb9e81b77f.jpg",
        "url": "https://www.verywellhealth.com/how-to-reduce-stress-5207327?"
    },
    {
        "title": "Doing this for 20 seconds each day could lead to major improvements to your mental health",
        "title_ru": "Выполнение этого упражнения в течение 20 секунд каждый день может помочь улучшить ваше психическое здоровье",
        "description": "Daily self-compassion and affirmations significantly boost emotional well-being and reduce stress, says UC Berkeley study.",
        "description_ru": "Ежедневное сострадание к себе и аффирмации значительно повышают эмоциональное благополучие и снижают стресс, говорится в исследовании Калифорнийского университета в Беркли.",
        "image_url": "https://nypost.com/wp-content/uploads/sites/2/2024/03/77871314.jpg?resize=2048,1365&quality=75&strip=all",
        "url": "https://nypost.com/2024/03/07/health/doing-this-for-20-seconds-each-day-could-lead-to-major-improvements-to-your-mental-health/?"
    },
    {
        "title": "Five easy tips for a happier life, from reducing social media to journaling",
        "title_ru": "Пять простых советов для более счастливой жизни: от сокращения использования социальных сетей до ведения дневника",
        "description": "Dr. Mark Rowe recommends keeping a gratitude journal, reducing social media, and mindfulness for better mental health.",
        "description_ru": "Доктор Марк Роу рекомендует вести дневник благодарности, сократить использование социальных сетей и проявлять осознанность для улучшения психического здоровья.",
        "image_url": "https://www.thesun.ie/wp-content/uploads/sites/3/2025/03/NINTCHDBPICT000980813063.jpg?strip=all&w=960",
        "url": "https://www.thesun.ie/health/14901425/reducing-social-media-journaling-tips-happiness-life/?"
    },
    {
        "title": "How to look after your mental health without spending a fortune",
        "title_ru": "Как позаботиться о своем психическом здоровье, не тратя при этом целое состояние",
        "description": "Outdoor activities, volunteering, and free resources are great ways to care for your mental health on a budget.",
        "description_ru": "Активный отдых на свежем воздухе, волонтерство и бесплатные ресурсы - отличные способы позаботиться о своем психическом здоровье с минимальными затратами.",
        "image_url": "https://i.guim.co.uk/img/media/ee6075cabcef6d9a4599dab0a4e75f4a593bf4af/0_0_5000_3000/master/5000.jpg?width=1300&dpr=2&s=none&crop=none",
        "url": "https://www.theguardian.com/money/2023/apr/09/how-to-look-after-your-mental-health-without-spending-a-fortune?"
    },
]

with app.app_context():
    for item in news_data:
        news = NewsPost(
            title=item["title"],
            title_ru=item["title_ru"],
            description=item["description"],
            description_ru=item["description_ru"],
            image_url=item["image_url"],
            url=item["url"]
        )
        db.session.add(news)
    db.session.commit()

