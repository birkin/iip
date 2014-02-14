"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

import pprint
from iip_search_app import common, forms
from django.test import TestCase


class CommonTest( TestCase ):

    def test_update_q_string( self ):
        """ Tests modification of solr query string. """
        initial_qstring = u'foo'
        log_identifier = u'bar'
        # no session_authz_dict
        session_authz_dict = None
        self.assertEqual(
            {'modified_qstring': u'display_status:(approved) AND foo'},
            common.updateQstring(initial_qstring, session_authz_dict, log_identifier) )
        # session_authz_dict, but no 'authorized' key
        session_authz_dict = { u'some_key': u'some_value' }
        self.assertEqual(
            {'modified_qstring': u'display_status:(approved) AND foo'},
            common.updateQstring(initial_qstring, session_authz_dict, log_identifier) )
        # session_authz_dict, and 'authorized' key, but authorized not True
        session_authz_dict = { u'authorized': u'other_than_true' }
        self.assertEqual(
            {'modified_qstring': u'display_status:(approved) AND foo'},
            common.updateQstring(initial_qstring, session_authz_dict, log_identifier) )
        # life good
        session_authz_dict = { u'authorized': True }
        self.assertEqual(
            {'modified_qstring': u'foo'},
            common.updateQstring(initial_qstring, session_authz_dict, log_identifier) )


class FormsTest( TestCase ):

    def test_facet_solr_query( self ):
        """ Checks type of data returned from query. """
        facet_count_dict = forms.facetResults( facet=u'placeMenu' )
        # pprint.pprint( facet_count_dict )
        for place in [  u'Galilee', u'Judaea', u'Lower Galilee' ]:
            self.assertEqual(
                place in facet_count_dict.keys(), True )
            self.assertEqual(
                type(facet_count_dict[place]) == int, True )


