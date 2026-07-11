import requests
import logging
import os
from dotenv import load_dotenv
logger = logging.getLogger(__name__)


class PipelineScheduler:
  def __init__(self, api_url: str, api_key: str) -> None:
    load_dotenv()
    self.PIPELINE_CRON_HOUR = os.getenv("PIPELINE_CRON_HOUR", "0")
    self.PIPELINE_CRON_MINUTE = os.getenv("PIPELINE_CRON_MINUTE", "0")
    self.scheduler = BackgroundScheduler()
    self.api_url = os.getenv("API_URL", api_url)
    self.api_key = os.getenv("API_KEY", api_key)
    

  def start(self) -> None:
    job_id = "pipeline-sync"
    cron_hour = self.PIPELINE_CRON_HOUR
    cron_minute = self.PIPELINE_CRON_MINUTE

    self.scheduler.add_job(
      self.run_pipeline,
      trigger="cron",
      hour=cron_hour,
      minute=cron_minute,
      id=job_id,
      replace_existing=True,
    )
    self.scheduler.start()

  def stop(self) -> None:
    if self.scheduler.running:
      self.scheduler.shutdown(wait=True)

  def run_pipeline(self) -> None:
    try:
      logger.info("Bắt đầu chạy pipeline sync...")

     
      response = requests.get(
        self.api_url,
        headers={"Authorization": f"Bearer {self.api_key}"},
        timeout=30,
      )
      response.raise_for_status()
      raw_data = response.json()

     
      transformed = self._transform(raw_data)

     
      self._load(transformed)

      logger.info("Pipeline chạy xong thành công.")

    except requests.RequestException as e:
      logger.error(f"Lỗi gọi API: {e}")
    except Exception as e:
      logger.error(f"Pipeline lỗi: {e}")
      raise

 