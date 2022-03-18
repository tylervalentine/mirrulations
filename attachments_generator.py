import os
import time
import dotenv
import redis
from mirrgen.search_iterator import SearchIterator
from mirrgen.results_processor import ResultsProcessor
from mirrcore.regulations_api import RegulationsAPI
from mirrcore.job_queue import JobQueue
from mirrcore.data_storage import DataStorage
from mirrcore.redis_check import is_redis_available

