import asyncio
import logging
import signal
import time
from collections.abc import Collection, MutableSequence

from dependency_injector.wiring import Provide, inject

from wan_manager.detectors.detector import Detector
from wan_manager.detectors.isp_detector import IspDetector


class Dispatcher:
    @inject
    def __init__(
        self, detectors: Collection[IspDetector] = Provide["detectors"]
    ) -> None:
        self.detectors = detectors
        self.detector_tasks: MutableSequence[asyncio.Task] = []
        self.logger = logging.getLogger(f"{__name__}:{self.__class__.__name__}")
        self._stopping = False

    async def run(self) -> None:
        self.logger.info("Starting dispatcher")

        self.detector_tasks = [
            asyncio.create_task(self.run_detector(detector))
            for detector in self.detectors
        ]

        asyncio.get_event_loop().add_signal_handler(signal.SIGTERM, self.stop)
        asyncio.get_event_loop().add_signal_handler(signal.SIGINT, self.stop)

        await asyncio.gather(*self.detector_tasks, return_exceptions=True)

        self.stop()

    def stop(self) -> None:
        if self._stopping:
            return

        self._stopping = True
        self.logger.info("Stopping dispatcher")
        for task in self.detector_tasks:
            task.cancel()
        self.detector_tasks.clear()
        self.logger.info("Dispatcher stopped")

    @staticmethod
    async def run_detector(detector: Detector) -> None:
        def get_sleep_time(last: float) -> float:
            time_took = time.time() - last
            return detector.freq.total_seconds() - time_took

        while True:
            time_start = time.time()
            try:
                await detector.run_once()
            except asyncio.CancelledError:
                break
            except Exception:
                detector.log.exception("Error executing detector run_once")

            await asyncio.sleep(get_sleep_time(time_start))
