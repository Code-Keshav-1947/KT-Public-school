"""Seed the database with sample notices and gallery images."""

from datetime import datetime, timedelta

from app import create_app
from app.extensions import db
from app.models import Notice, GalleryImage


def seed():
    app = create_app()
    with app.app_context():
        db.create_all()

        if Notice.query.first():
            print("Database already has data. Skipping seed.")
            return

        now = datetime.utcnow()

        notices = [
            Notice(
                title="Admissions Open for 2026–27 Academic Session",
                body=(
                    "We are pleased to announce that admissions for the academic session 2026–27 "
                    "are now open for Nursery through Class X.\n\n"
                    "Interested parents are requested to submit the online inquiry form or visit "
                    "the school office between 9:00 AM and 2:00 PM on working days.\n\n"
                    "Required documents: Birth certificate, previous report card (if applicable), "
                    "and address proof."
                ),
                published_at=now - timedelta(days=2),
            ),
            Notice(
                title="Annual Sports Day — 15 September 2026",
                body=(
                    "KT Public School will celebrate its Annual Sports Day on 15 September 2026. "
                    "All parents are cordially invited to witness the event and cheer for our young athletes.\n\n"
                    "Schedule:\n"
                    "- 8:30 AM — Opening ceremony\n"
                    "- 9:00 AM — Track and field events\n"
                    "- 12:00 PM — Prize distribution\n\n"
                    "Students must come in their sports uniform."
                ),
                published_at=now - timedelta(days=5),
            ),
            Notice(
                title="Parent-Teacher Meeting — 25 August 2026",
                body=(
                    "A Parent-Teacher Meeting is scheduled for 25 August 2026 from 10:00 AM to 1:00 PM. "
                    "All parents are encouraged to attend and discuss their child's progress with class teachers.\n\n"
                    "Please carry your child's school ID card for entry."
                ),
                published_at=now - timedelta(days=10),
            ),
        ]

        gallery = [
            GalleryImage(
                title="Annual Day Celebration",
                image_path="img/gallery/annual_day.svg",
                caption="Students performing at the Annual Day function",
            ),
            GalleryImage(
                title="Sports Day",
                image_path="img/gallery/sports_day.svg",
                caption="Inter-house athletics competition",
            ),
            GalleryImage(
                title="Science Exhibition",
                image_path="img/gallery/science_exhibition.svg",
                caption="Students showcasing science projects",
            ),
        ]

        db.session.add_all(notices + gallery)
        db.session.commit()
        print("Database seeded successfully!")


if __name__ == "__main__":
    seed()
