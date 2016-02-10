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

class TestArcReview(BlankDB):
    def test_empty_arc_review(self):
        response = self.client.get("/api/arcreviews/")
        self.assertEqual(response.json, {"arcReviews" : []})
        
    def test_arc_review_no_id(self):
        response = self.client.get("/api/arcreviews/1/")
        self.assertEqual(response.json, {"Error" : "ArcReviewID 1 not found"})
    
    def test_create_arc_review(self):
        response = self.client.post("/api/arcreviews/", data = {
            "projectID" : 1,
            "review_type" : 1,
            "date_sent_to_reviewer" : "2016-02-02",
            "reviewer1" : 1,
            "reviewer1_rec" : 1,
            "reviewer1_sig_date" : "2016-02-02",
            "reviewer1_comments" : "test comment",
            "reviewer2" : 2,
            "reviewer2_rec"  :2 ,
            "reviewer2_sig_date" : "2016-02-02",
            "reviewer2_comments" : "2016-02-02",
            "research" : 1,
            "lnkage":False,
            "contact" : True,
            "engaged" : True,
            "non_public_data" : True
        })
        self.assertEqual(response.json, {"arcReviewID" : 1})
            
class TestBudget(BlankDB):
    def test_empty_budget(self):
        response = self.client.get("/api/budgets/")
        self.assertEqual(response.json, {"budgets" : [] })
        
    def test_budget_no_id(self):
        response = self.client.get('/api/budgets/1/')
        self.assertEqual(response.json, {"Error" : "BudgetID 1 not found"})
        
    def test_create_budget(self):
        response = self.client.post("/api/budgets/", data = {
            "projectID" : 1,
            "numPeriods" : 2,
            "periodStart" : "2016-02-02",
            "periodEnd" : "2016-02-02",
            "periodTotal" : 1.2,
            "periodComment" : "comment"
        })
        self.assertEqual(response.json, dict(budgetID=1))
 
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

class TestReviewCommittee(BlankDB):
    def test_empty_review_committee(self):
        response = self.client.get("/api/reviewcommittees/")
        self.assertEqual(response.json, dict(reviewCommittees = []))
        
    def test_review_committee_no_id(self):
        response = self.client.get("/api/reviewcommittees/1/")
        self.assertEqual(response.json, {"Error": "ReviewCommitteeID 1 not found"})
        
    def test_create_review_committee(self):
        response = self.client.post("/api/reviewcommittees/", data = {
            "project_projectID" : 1,
            "RCStatusList_rc_StatusID": 1,
            "reviewCommitteeList_rcListID": 1,
            "review_committee_number":"1",
            "date_initial_review":"2016-02-02",
            "date_expires" : "2016-02-02",
            "rc_note" : "rc_note",
            "rc_protocol" : "rc_proto",
            "rc_approval":"rc_approval"
        })
        self.assertEqual(response.json, {"reviewCommitteeID" : 1})
        
class TestReviewCommitteeList(BlankDB):
    def test_empty_review_committee_lists(self):
        response = self.client.get("/api/reviewcommitteelist/")
        self.assertEqual(response.json, dict(reviewCommitteeList = []))
        
    def test_review_committee_list_no_id(self):
        response = self.client.get("/api/reviewcommitteelist/1/")
        self.assertEqual(response.json, {"Error": "RCListID 1 not found"})
        
    def test_create_review_committee_list(self):
        response = self.client.post("/api/reviewcommitteelist/", data = {
            "reviewCommittee" : "rc test",
            "rc_description" : "rc desc"
            })
        self.assertEqual(response.json, {"rcListID" : 1 })

class TestUCRReport(BlankDB):
    def test_empty_ucr_report(self):
        response = self.client.get("/api/ucrreports/")
        self.assertEqual(response.json, dict(ucrReports = []))
        
    def test_ucr_report_no_id(self):
        response = self.client.get("/api/ucrreports/1/")
        self.assertEqual(response.json, {"Error": "UcrReportID 1 not found"})
        
    def test_create_ucr_report(self):
        response = self.client.post("/api/ucrreports/", data = {
            "projectID" : 1,
            "report_type" : 1,
            "report_submitted" : "2016-02-02",
            "report_due" : "2016-02-02",
            "report_doc" : "doc"
        })
        self.assertEqual(response.json, {"ucrReportID" : 1})
        
if __name__ == '__main__':
    unittest.main()
    