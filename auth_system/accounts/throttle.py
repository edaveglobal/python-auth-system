from rest_framework.throttling import AnonRateThrottle, UserRateThrottle

class AnonRateThreeMinutesThrottle(AnonRateThrottle):
    """ Custom Anonymous API Rate Limiting"""
    
    def parse_rate(self, rate):
        """
            Given the request rate string, return a two tuple of:
            <allowed number of requests>, <period of time in seconds>

            So we always return a rate for 2 requests per 3 minutes.

            Args:
                string: rate to be parsed, which we ignore.

            Returns:
                tuple:  <allowed number of requests>, <period of time in seconds>
        """
        return (2, 180)
    
    # def allow_request(self, request, view):
    #     if request.method == "GET":
    #         return True
    #     return super().allow_request(request, view)
        
        

class UserRateOnePerDayThrottle(UserRateThrottle):
    """ Custom Anonymous API Rate Limiting"""
    
    def parse_rate(self, rate):
        """
            Given the request rate string, return a two tuple of:
            <allowed number of requests>, <period of time in seconds>

            So we always return a rate for 1 request per day.

            Args:
                string: rate to be parsed, which we ignore.

            Returns:
                tuple:  <allowed number of requests>, <period of time in seconds>
        """
        return (2, 86400)
    
    # def allow_request(self, request, view):
    #     if request.method != "GET" and request.method != "PUT":
    #         return True
    #     return super().allow_request(request, view)