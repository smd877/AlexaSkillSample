# -*- coding: utf-8 -*-

import logging
import json

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import (
    AbstractRequestHandler, AbstractExceptionHandler,
    AbstractRequestInterceptor, AbstractResponseInterceptor)
from ask_sdk_core.utils import is_request_type, is_intent_name, get_slot_value
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model.ui import SimpleCard
from ask_sdk_model import Response

sb = SkillBuilder()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Built-in Intent Handlers
class GetNewFactHandler(AbstractRequestHandler):
    """Handler for Skill Launch and GetNewFact Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_request_type("LaunchRequest")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In GetNewFactHandler")

        speech = "元気？「はい」か「いいえ」で答えてね！"

        handler_input.response_builder.speak(speech).set_card(
            SimpleCard("GetNewFactHandler", speech)).set_should_end_session(False)
        return handler_input.response_builder.response


class OtherHandler(AbstractRequestHandler):
    """Handler for Help Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_intent_name("AMAZON.HelpIntent")(handler_input) or
            is_intent_name("AMAZON.CancelIntent")(handler_input) or
            is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In OtherHandler")

        speech = "ヘルプかキャンセルかストップが呼ばれた！"
        handler_input.response_builder.speak(speech).set_card(
            SimpleCard("OtherHandler", speech))
        return handler_input.response_builder.response


class ReplyHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("ReplyIntent")(handler_input)

    def handle(self, handler_input):
        reply_msg = get_slot_value(handler_input=handler_input, slot_name="reply_message")
        if reply_msg == 'はい':
            speech_text = "イェーイ！"
            end_session = True
        elif reply_msg == 'いいえ':
            speech_text = "ファイト！"
            end_session = True
        else:
            speech_text = "「はい」か「いいえ」で答えてね！"
            end_session = False
        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("ReplyHandler", speech_text)).set_should_end_session(end_session)
        return handler_input.response_builder.response


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In SessionEndedRequestHandler")

        logger.info("Session ended reason: {}".format(
            handler_input.request_envelope.request.reason))
        return handler_input.response_builder.response


# Request and Response loggers
class RequestLogger(AbstractRequestInterceptor):
    """Log the alexa requests."""

    def process(self, handler_input):
        # type: (HandlerInput) -> None
        logger.debug("Alexa Request: {}".format(
            handler_input.request_envelope.request))


class ResponseLogger(AbstractResponseInterceptor):
    """Log the alexa responses."""

    def process(self, handler_input, response):
        # type: (HandlerInput, Response) -> None
        logger.debug("Alexa Response: {}".format(response))


# Register intent handlers
sb.add_request_handler(GetNewFactHandler())
sb.add_request_handler(OtherHandler())
sb.add_request_handler(ReplyHandler())
sb.add_request_handler(SessionEndedRequestHandler())

# Register request and response interceptors
sb.add_global_request_interceptor(RequestLogger())
sb.add_global_response_interceptor(ResponseLogger())

# Handler name that is used on AWS lambda
lambda_handler = sb.lambda_handler()
