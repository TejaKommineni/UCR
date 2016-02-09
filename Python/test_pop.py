import unittest
from flask.ext.testing import TestCase
import app
from app.database import db
from datetime import datetime
import app.models as models

    
###################################################################################################
# Populated database
###################################################################################################
        
class PopulatedDB(TestCase):
    def create_app(self):
        # pass in test configuration
        return app.create_app('test_config')

    def setUp(self):
        db.create_all()
        self.populate_db()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        
    def populate_db(self):
        arcReview = models.ArcReview(
            review_type = 1,
            date_sent_to_reviewer = datetime(2016,2,2),
            reviewer1 = 1,
            reviewer1_rec = 1,
            reviewer1_sig_date = datetime(2016,2,2),
            reviewer1_comments = "test comment",
            reviewer2 = 2,
            reviewer2_rec  =2 ,
            reviewer2_sig_date = datetime(2016,2,2),
            reviewer2_comments = datetime(2016,2,2),
            research = 1,
            lnkage=False,
            contact = True,
            engaged = True,
            non_public_data = True)
            
        budget = models.Budget(
            numPeriods = 1,
            periodStart = datetime(2016,2,2),
            periodEnd = datetime(2016,2,2),
            periodTotal = 1.23,
            periodComment = "Budget Period")
            
        p = models.Project(
            projectType_projectTypeID = 1,
            IRBHolderLUT_irbHolderID = 1,
            project_name = "Test Project",
            short_title = "Test Project",
            project_summary = "Summary",
            sop="sop",
            UCR_proposal="ucr_proposal",
            budget_doc = "budget_doc",
            UCR_fee = "no",
            UCR_no_fee = "yes",
            budget_end_date = datetime(2016,2,2),
            previous_short_title = "t short",
            date_added = datetime(2016,2,2),
            final_recruitment_report = "report")
        rc = models.ReviewCommittee(
            project_projectID=p.projectID,
            review_committee_number=1,
            date_initial_review=datetime(2016,2,2),
            date_expires = datetime(2016,2,2),
            rc_note = "rc_note",
            rc_protocol = "rc_proto",
            rc_approval="rc_approval")
        
        rcsl = models.RCStatusList(
            rc_status = "Status 1",
            rc_status_definition = "rc status def")
            
        irb = models.IRBHolderLUT(
            irb_holder = "holder 1",
            irb_holder_definition= "IRB 1")
            
        rcl = models.ReviewCommitteeList(
            reviewCommittee = "rc",
            rc_description = "rc desc")
            
        pt = models.ProjectType(
            project_type = "Type 1",
            project_type_definition = "Def 1")
        
        rc.RCStatusList = rcsl
        rc.reviewCommitteeList = rcl
        p.irbHolder = irb
        p.projectType = pt
        p.reviewCommittees.append(rc)
        p.budgets.append(budget)
        p.arcReview = arcReview

        db.session.add(p)
        db.session.commit()
        
##############################################################################
# Root Node Tests
##############################################################################
class TestRoot(PopulatedDB):
    def test_root(self):
        response = self.client.get("/api/")
        self.assertEqual(response.json, {
            "version" : 0.01,
            "endpoints" : [
                "projects",
                "staff"
            ]})    

##############################################################################
# IRB Holder Tests
##############################################################################
class TestIRBHolder(PopulatedDB):
    def test_get_irb_holders(self):
        response = self.client.get("/api/irbholders/")
        self.assertEqual(response.json["irbHolders"][0]["irb_holder"],"holder 1")
        self.assertEqual(response.json["irbHolders"][0]["irb_holder_definition"],"IRB 1")
        
    def test_get_irb_holder(self):
        response = self.client.get("/api/irbholders/1/")
        self.assertEqual(response.json["irb_holder"],"holder 1")
        self.assertEqual(response.json["irb_holder_definition"],"IRB 1")
        
    def test_update_irb_holder(self):
        response = self.client.put("/api/irbholders/1/", data = {
            "irb_holder" : "holder 1 Updated",
            "irb_holder_definition" : "IRB 1 Updated"
        })
        self.assertEqual(response.json["irb_holder"],"holder 1 Updated")
        self.assertEqual(response.json["irb_holder_definition"],"IRB 1 Updated")
        
    def test_delete_irb_holder(self):
        response = self.client.delete("/api/irbholders/1/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "IrbHolderID 1 deleted")
            
##############################################################################
# Project Tests
##############################################################################
class TestProject(PopulatedDB):   
    # test getting list of projects
    def test_get_projects(self):
        response = self.client.get("/api/projects/")
        self.assertEqual(response.json["projects"][0]["projectID"],1)
        self.assertEqual(response.json["projects"][0]["projectType_projectTypeID"],1)
        self.assertEqual(response.json["projects"][0]["IRBHolderLUT_irbHolderID"],1)
        self.assertEqual(response.json["projects"][0]["project_name"],"Test Project")
        self.assertEqual(response.json["projects"][0]["short_title"],"Test Project")
        self.assertEqual(response.json["projects"][0]["project_summary"],"Summary")
        self.assertEqual(response.json["projects"][0]["sop"],"sop")
        self.assertEqual(response.json["projects"][0]["UCR_proposal"],"ucr_proposal")
        self.assertEqual(response.json["projects"][0]["budget_doc"],"budget_doc")
        self.assertEqual(response.json["projects"][0]["UCR_fee"],"no")
        self.assertEqual(response.json["projects"][0]["UCR_no_fee"],"yes")
        self.assertEqual(response.json["projects"][0]["budget_end_date"],"2016-02-02")
        self.assertEqual(response.json["projects"][0]["previous_short_title"],"t short")
        self.assertEqual(response.json["projects"][0]["date_added"],"2016-02-02")
        self.assertEqual(response.json["projects"][0]["final_recruitment_report"],"report")
    # Test getting single project
    def test_get_project(self):
        response = self.client.get("/api/projects/1/")
        self.assertEqual(response.json["projectID"],1)
        self.assertEqual(response.json["projectType_projectTypeID"],1)
        self.assertEqual(response.json["IRBHolderLUT_irbHolderID"],1)
        self.assertEqual(response.json["project_name"],"Test Project")
        self.assertEqual(response.json["short_title"],"Test Project")
        self.assertEqual(response.json["project_summary"],"Summary")
        self.assertEqual(response.json["sop"],"sop")
        self.assertEqual(response.json["UCR_proposal"],"ucr_proposal")
        self.assertEqual(response.json["budget_doc"],"budget_doc")
        self.assertEqual(response.json["UCR_fee"],"no")
        self.assertEqual(response.json["UCR_no_fee"],"yes")
        self.assertEqual(response.json["budget_end_date"],"2016-02-02")
        self.assertEqual(response.json["previous_short_title"],"t short")
        self.assertEqual(response.json["date_added"],"2016-02-02")
        self.assertEqual(response.json["final_recruitment_report"],"report")
    # Test update project
    def test_update_project(self):
        response = self.client.put("/api/projects/1/",data = {
            "projectType_projectTypeID" : 2,
            "IRBHolderLUT_irbHolderID" : 2,
            "project_name" : "Test Project Update",
            "short_title" : "Test Project Update",
            "project_summary" : "Summary Update",
            "sop":"sop Update",
            "UCR_proposal":"ucr_proposal Update",
            "budget_doc" : "budget_doc Update",
            "UCR_fee" : "no Update",
            "UCR_no_fee" : "yes Update",
            "budget_end_date" : "2016-02-03",
            "previous_short_title" : "t short Update",
            "date_added" : "2016-02-03",
            "final_recruitment_report" : "report Update"
        })
        self.assertEqual(response.json["projectID"],1)
        self.assertEqual(response.json["projectType_projectTypeID"],2)
        self.assertEqual(response.json["IRBHolderLUT_irbHolderID"],2)
        self.assertEqual(response.json["project_name"],"Test Project Update")
        self.assertEqual(response.json["short_title"],"Test Project Update")
        self.assertEqual(response.json["project_summary"],"Summary Update")
        self.assertEqual(response.json["sop"],"sop Update")
        self.assertEqual(response.json["UCR_proposal"],"ucr_proposal Update")
        self.assertEqual(response.json["budget_doc"],"budget_doc Update")
        self.assertEqual(response.json["UCR_fee"],"no Update")
        self.assertEqual(response.json["UCR_no_fee"],"yes Update")
        self.assertEqual(response.json["budget_end_date"],"2016-02-03")
        self.assertEqual(response.json["previous_short_title"],"t short Update")
        self.assertEqual(response.json["date_added"],"2016-02-03")
        self.assertEqual(response.json["final_recruitment_report"],"report Update")
        
     # Test deletetion of project
    def test_delete_project(self):
        response = self.client.delete("/api/projects/1/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "ProjectID 1 deleted")

##############################################################################
# RCStatusList Tests
##############################################################################
class TestRCStatusList(PopulatedDB):
    def test_get_rcStatusList(self):
        response = self.client.get("/api/rcstatuslist/")
        self.assertEqual(response.json["RCStatusList"][0]["rcStatusID"], 1)
        self.assertEqual(response.json["RCStatusList"][0]["rc_status"], "Status 1")
        self.assertEqual(response.json["RCStatusList"][0]["rc_status_definition"], "rc status def")
        
    def test_get_rcStatus(self):
        response = self.client.get("/api/rcstatuslist/1/")
        self.assertEqual(response.json["rcStatusID"], 1)
        self.assertEqual(response.json["rc_status"], "Status 1")
        self.assertEqual(response.json["rc_status_definition"], "rc status def")
        
    def test_update_rcStatus(self):
        response = self.client.put("/api/rcstatuslist/1/", data = {
            "rc_status" : "Status 1 Updated",
            "rc_status_definition" : "rc status def Updated"
        })
        self.assertEqual(response.json["rcStatusID"], 1)
        self.assertEqual(response.json["rc_status"], "Status 1 Updated")
        self.assertEqual(response.json["rc_status_definition"], "rc status def Updated")
        
    def test_delete_rcStatusList(self):
        response = self.client.delete("/api/rcstatuslist/1/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "RCStatusListID 1 deleted")
        
##############################################################################
# ReviewCommitteList
##############################################################################
class TestReviewCommitteeList(PopulatedDB):
    def test_get_review_committee_lists(self):
        response = self.client.get("/api/reviewcommitteelist/")
        self.assertEqual(response.json["ReviewCommitteeList"][0]["reviewCommittee"], "rc")
        self.assertEqual(response.json["ReviewCommitteeList"][0]["rc_description"], "rc desc")
        
    def test_get_review_committee_list(self):
        response = self.client.get("/api/reviewcommitteelist/1/")
        self.assertEqual(response.json["reviewCommittee"], "rc")
        self.assertEqual(response.json["rc_description"], "rc desc")
        
    def test_update_review_committee_list(self):
        response = self.client.put("/api/reviewcommitteelist/1/", data = {
            "reviewCommittee" : "rc Updated",
            "rc_description" : "rc desc Updated"
            })
        self.assertEquals(response.json["reviewCommittee"],"rc Updated")
        self.assertEquals(response.json["rc_description"],"rc desc Updated")
        
    def test_delete_review_committee_list(self):
        response = self.client.delete("/api/reviewcommitteelist/1/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "RCListID 1 deleted")
        
if __name__ == '__main__':
    unittest.main()