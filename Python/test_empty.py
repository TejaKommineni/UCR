import unittest
from flask.ext.testing import TestCase
import app
from app.database import db
from datetime import datetime
import app.models as models

"""
    A suite of tests to run when there is blank database
    
    - Get root node
    - Get empty responses
    - Add data
   
    Creates all tables from scratch before each test,
    Dumps all tables at the end of each test
   
"""
class BlankDB(TestCase):
    def create_app(self):
        # pass in test configuration
        return app.create_app('test_config')

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
##############################################################################
# Root Node Tests
##############################################################################
class TestRoot(BlankDB):        
    # Test the root node    
    def test_root(self):
        response = self.client.get("/api/")
        self.assertEqual(response.json, {
            "version" : 0.01,
            "endpoints" : [
                "projects",
                "staff"
            ]})

#############################################################################
# IRB Holder Tests
#############################################################################
class TestIRBHolder(BlankDB):
    def test_empty_irb_holder(self):
        response = self.client.get("/api/irbholders/")
        self.assertEqual(response.json, {"irbHolders" : []})
    
    def test_irb_holder_no_id(self):
        response = self.client.get("/api/irbholders/1/")
        self.assertEqual(response.json, {"Error" : "IrbHolderID 1 not found"})
        
    def test_create_irb_holder(self):
        response = self.client.post("/api/irbholders/", data = {
            "irb_holder" : "test holder",
            "irb_holder_definition" : "test holder def"
            })
        self.assertEqual(response.json, dict(irbHolderID=1))
       
##############################################################################
# Project Tests
##############################################################################   
class TestProject(BlankDB):
    # Test for empty array of projects        
    def test_empty_projects(self):
        response = self.client.get("/api/projects/")
        self.assertEqual(response.json, {
            "projects":[]
            })
    # Test for project not found        
    def test_project_no_id(self):
        response = self.client.get("/api/projects/1/")
        self.assertEqual(response.json, {"Error" : 
            "ProjectID 1 not found"})
    # Test create a project
    # TODO: insert foreign key items first (SQLITE doesn't care) 
    def test_create_project(self):
        response = self.client.post("/api/projects/", data = {
            "projectType_projectTypeID" : 1,
            "IRBHolderLUT_irbHolderID" : 1,
            "project_name" : "Test Project",
            "short_title" : "Test Project",
            "project_summary" : "Summary",
            "sop":"sop",
            "UCR_proposal":"ucr_proposal",
            "budget_doc" : "budget_doc",
            "UCR_fee" : "no",
            "UCR_no_fee" : "yes",
            "budget_end_date" : "2016-02-02",
            "previous_short_title" : "t short",
            "date_added" : "2016-02-02",
            "final_recruitment_report" : "report"})
        self.assertEqual(response.json,dict(projectID=1))
        
##############################################################################
# RCStatusList Tests
##############################################################################
class TestRCStatusList(BlankDB):
    # Test for empty RCStatusList
    def test_empty_rcStatusList(self):
        response = self.client.get("/api/rcstatuslist/")
        self.assertEqual(response.json, dict(RCStatusList = []))
    # Test for rcStatusList not found    
    def test_rcStatusList_no_id(self):
        response = self.client.get("/api/rcstatuslist/1/")
        self.assertEqual(response.json, {"Error" : "RCStatusID 1 not found"})
    # Test create RCStatusList
    def test_create_rcStatusList(self):
        response = self.client.post("/api/rcstatuslist/", data = {
            "rc_status" : "Status 1",
            "rc_status_definition" : "rc status def"
        })
        self.assertEqual(response.json, {"rcStatusListID": 1})
        
##############################################################################
# ReviewCommitteList Tests
##############################################################################
class TestReviewCommitteeList(BlankDB):
    def test_empty_review_committee_lists(self):
        response = self.client.get("/api/reviewcommitteelist/")
        self.assertEqual(response.json, dict(ReviewCommitteeList = []))
        
    def test_review_committee_list_no_id(self):
        response = self.client.get("/api/reviewcommitteelist/1/")
        self.assertEqual(response.json, {"Error": "RCListID 1 not found"})
        
    def test_create_review_committee_list(self):
        response = self.client.post("/api/reviewcommitteelist/", data = {
            "reviewCommittee" : "rc test",
            "rc_description" : "rc desc"
            })
        self.assertEqual(response.json, {"rcListID" : 1 })
        
if __name__ == '__main__':
    unittest.main()
    