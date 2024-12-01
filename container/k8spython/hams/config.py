
import asyncio
import aiohttp
import logging
from typing import List, Union
from pydantic import Field, BaseModel
from pydantic import HttpUrl
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


class HamsCheck(ABC, BaseModel):
    """
    call for a preflight or shutdown
    """
    name: str = Field(description="Name of the check")
    description: str = Field(description="Description of the check")


    async def check(self) -> bool:
        """
        Safe check to run the check
        """
        try:
            check_response = await self.run_check()
            logger.info(f"Check[{self.name}]: {"PASSED" if check_response else "FAILED"}")

            return check_response
        except Exception as e:
            logger.info(f"Check[{self.name}]: {e}")
            return False


    @abstractmethod
    async def run_check(self) -> bool:
        pass


class HttpCheck(HamsCheck):
    """
    Check that a URL is reachable
    """
    http: HttpUrl = Field(description="URL to check")
    returncode: int = Field(default=200, description="Expected return code")

    async def run_check(self) -> bool:
        logger.debug(f"HttpCheck[{self.name}]: {self.http} == {self.returncode}")

        async with aiohttp.ClientSession() as session:
            async with session.get(str(self.http)) as response:
                return response.status == self.returncode



CheckType = Union[HttpCheck]



class HamsChecks(BaseModel):
    """
    preflight and shutdown calls for the service
    Check that certain actions are in place before we start the service fully
    When we shutdown run a set of shutdown actions
    """
    timeout: int = Field(description="Timeout for the check")
    fails: int = Field(description="Number of fails before the check is considered failed")
    preflights: List[CheckType] = Field(description="Preflight checks")
    shutdowns: List[CheckType] = Field(description="Shutdown checks")

    async def run_checks(self, checks: List[CheckType]) -> bool:
        """
        Run the checks with timeouts and fail counting
        Will reply True if all checks pass
        Will reply False if tests consistently fail for all attempts
        """
        remaining_attempts = self.fails
        while remaining_attempts > 0:
            if all([await check.check() for check in checks]):
                return True
            remaining_attempts -= 1
            if remaining_attempts>0:
                await asyncio.sleep(self.timeout)

        logger.error(f"Checks failed")

        raise Exception("Checks failed")
        return False


    async def run_preflights(self):
        results = await self.run_checks(self.preflights)



class HamsConfig(BaseModel):
    url: HttpUrl = Field(description="Host to listen for health and monitoring")
    prefix: str = Field(description="Prefix for the name of the resources")
    checks: HamsChecks = Field(description="Health and monitoring checks")
