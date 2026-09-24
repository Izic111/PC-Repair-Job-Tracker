from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///jobs.db"
db = SQLAlchemy(app)


class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(30))
    device = db.Column(db.String(100), nullable=False)
    issue = db.Column(db.String(300), nullable=False)
    status = db.Column(db.String(20), default="Received")  # Received / In Progress / Done
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "client_name": self.client_name,
            "phone": self.phone,
            "device": self.device,
            "issue": self.issue,
            "status": self.status,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M"),
        }


with app.app_context():
    db.create_all()


@app.route("/jobs", methods=["GET"])
def get_jobs():
    jobs = Job.query.order_by(Job.created_at.desc()).all()
    return jsonify([j.to_dict() for j in jobs])


@app.route("/jobs", methods=["POST"])
def create_job():
    data = request.get_json() or {}

    required = ["client_name", "device", "issue"]
    missing = [f for f in required if not data.get(f)]
    if missing:
        return jsonify({"error": f"Missing required fields: {', '.join(missing)}"}), 400

    job = Job(
        client_name=data["client_name"],
        phone=data.get("phone", ""),
        device=data["device"],
        issue=data["issue"],
        status=data.get("status", "Received"),
    )
    db.session.add(job)
    db.session.commit()
    return jsonify(job.to_dict()), 201


@app.route("/jobs/<int:job_id>", methods=["PUT"])
def update_job(job_id):
    job = Job.query.get(job_id)
    if not job:
        return jsonify({"error": "Job not found"}), 404

    data = request.get_json() or {}
    if "status" in data:
        if data["status"] not in ("Received", "In Progress", "Done"):
            return jsonify({"error": "Invalid status"}), 400
        job.status = data["status"]
    for field in ("client_name", "phone", "device", "issue"):
        if field in data:
            setattr(job, field, data[field])

    db.session.commit()
    return jsonify(job.to_dict())


@app.route("/jobs/<int:job_id>", methods=["DELETE"])
def delete_job(job_id):
    job = Job.query.get(job_id)
    if not job:
        return jsonify({"error": "Job not found"}), 404

    db.session.delete(job)
    db.session.commit()
    return jsonify({"deleted": job_id})


@app.route("/", methods=["GET"])
def health_check():
    return jsonify({"status": "ok", "service": "PC Repair Job Tracker API"})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
