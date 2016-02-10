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
            reviewer2_comments = "test comment",
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
            periodComment = "comment")
            
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
            RCStatusList_rc_StatusID=1,
            reviewCommitteeList_rcListID=1,
            review_committee_number="1",
            date_initial_review=datetime(2016,2,2),
            date_expires = datetime(2016,2,2),
            rc_note = "rc_note",
            rc_protocol = "rc_proto",
            rc_approval="rc_approval")
            
        ucr = models.UCRReport(
            projectID = 1,
            report_type= 1,
            report_submitted= datetime(2016,2,2),
            report_due= datetime(2016,2,2),
            report_doc= "doc"
        )
        
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
        p.ucrReports.append(ucr)

        db.session.add(p)
        db.session.commit()
        
class TestRoot(PopulatedDB):
    def test_root(self):
        response = self.client.get("/api/")
        self.assertEqual(response.json, {
            "version" : 0.01,
            "endpoints" : [
                "projects",
                "staff"
            ]})    

class TestArcReview(PopulatedDB):
    def test_get_arc_reviews(self):
        response = self.client.get("/api/arcreviews/")
        self.assertEqual(response.json["arcReviews"][0]["projectID"], 1)
        self.assertEqual(response.json["arcReviews"][0]["review_type"], 1)
        self.assertEqual(response.json["arcReviews"][0]["date_sent_to_reviewer"], "2016-02-02")
        self.assertEqual(response.json["arcReviews"][0]["reviewer1"], 1)
        self.assertEqual(response.json["arcReviews"][0]["reviewer1_rec"], 1)
        self.assertEqual(response.json["arcReviews"][0]["reviewer1_sig_date"], "2016-02-02")
        self.assertEqual(response.json["arcReviews"][0]["reviewer1_comments"], "test comment")
        self.assertEqual(response.json["arcReviews"][0]["reviewer2"], 2)
        self.assertEqual(response.json["arcReviews"][0]["reviewer2_rec"], 2)
        self.assertEqual(response.json["arcReviews"][0]["reviewer2_sig_date"], "2016-02-02")
        self.assertEqual(response.json["arcReviews"][0]["reviewer2_comments"], "test comment")
        self.assertEqual(response.json["arcReviews"][0]["research"], 1)
        self.assertEqual(response.json["arcReviews"][0]["contact"], True)
        self.assertEqual(response.json["arcReviews"][0]["lnkage"], False)
        self.assertEqual(response.json["arcReviews"][0]["engaged"], True)
        self.assertEqual(response.json["arcReviews"][0]["non_public_data"], True)
        
    def test_get_arc_review(self):
        response = self.client.get("/api/arcreviews/1/")
        self.assertEqual(response.json["projectID"], 1)
        self.assertEqual(response.json["review_type"], 1)
        self.assertEqual(response.json["date_sent_to_reviewer"], "2016-02-02")
        self.assertEqual(response.json["reviewer1"], 1)
        self.assertEqual(response.json["reviewer1_rec"], 1)
        self.assertEqual(response.json["reviewer1_sig_date"], "2016-02-02")
        self.assertEqual(response.json["reviewer1_comments"], "test comment")
        self.assertEqual(response.json["reviewer2"], 2)
        self.assertEqual(response.json["reviewer2_rec"], 2)
        self.assertEqual(response.json["reviewer2_sig_date"], "2016-02-02")
        self.assertEqual(response.json["reviewer2_comments"], "test comment")
        self.assertEqual(response.json["research"], 1)
        self.assertEqual(response.json["contact"], True)
        self.assertEqual(response.json["lnkage"], False)
        self.assertEqual(response.json["engaged"], True)
        self.assertEqual(response.json["non_public_data"], True)
        
    def test_update_arc_review(self):
        response = self.client.put("/api/arcreviews/1/", data = {
            "projectID" : 2,
            "review_type" : 2,
            "date_sent_to_reviewer" : "2016-02-03",
            "reviewer1" : 3,
            "reviewer1_rec" : 3,
            "reviewer1_sig_date" : "2016-02-03",
            "reviewer1_comments" : "test comment Updated",
            "reviewer2" : 4,
            "reviewer2_rec"  :4 ,
            "reviewer2_sig_date" : "2016-02-03",
            "reviewer2_comments" : "test comment Updated",
            "research" : 2,
            "lnkage":True,
            "contact" : False,
            "engaged" : False,
            "non_public_data" : False
        })
        print(response.json)
        self.assertEqual(response.json["projectID"], 2)
        self.assertEqual(response.json["review_type"], 2)
        self.assertEqual(response.json["date_sent_to_reviewer"], "2016-02-03")
        self.assertEqual(response.json["reviewer1"], 3)
        self.assertEqual(response.json["reviewer1_rec"], 3)
        self.assertEqual(response.json["reviewer1_sig_date"], "2016-02-03")
        self.assertEqual(response.json["reviewer1_comments"], "test comment Updated")
        self.assertEqual(response.json["reviewer2"], 4)
        self.assertEqual(response.json["reviewer2_rec"], 4)
        self.assertEqual(response.json["reviewer2_sig_date"], "2016-02-03")
        self.assertEqual(response.json["reviewer2_comments"], "test comment Updated")
        self.assertEqual(response.json["research"], 2)
        self.assertEqual(response.json["contact"], False)
        self.assertEqual(response.json["lnkage"], True)
        self.assertEqual(response.json["engaged"], False)
        self.assertEqual(response.json["non_public_data"], False)
        
    def test_delete_arc_review(self):
        response = self.client.delete("/api/arcreviews/1/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "ArcReviewID 1 deleted")
            
class TestBudget(PopulatedDB):
    def test_get_budgets(self):
        response = self.client.get("/api/budgets/")
        self.assertEqual(response.json["budgets"][0]["projectID"], 1)
        self.assertEqual(response.json["budgets"][0]["numPeriods"], 1)
        self.assertEqual(response.json["budgets"][0]["periodStart"], "2016-02-02")
        self.assertEqual(response.json["budgets"][0]["periodEnd"], "2016-02-02")
        self.assertEqual(response.json["budgets"][0]["periodTotal"], 1.23)
        self.assertEqual(response.json["budgets"][0]["periodComment"], "comment")
        
    def test_get_budget(self):
        response = self.client.get("/api/budgets/1/")
        self.assertEqual(response.json["projectID"], 1)
        self.assertEqual(response.json["numPeriods"], 1)
        self.assertEqual(response.json["periodStart"], "2016-02-02")
        self.assertEqual(response.json["periodEnd"], "2016-02-02")
        self.assertEqual(response.json["periodTotal"], 1.23)
        self.assertEqual(response.json["periodComment"], "comment")
        
    def test_update_budget(self):
        response = self.client.put("/api/budgets/1/",data = {
            "projectID" : 2,
            "numPeriods" : 2,
            "periodStart" : "2016-02-03",
            "periodEnd" : "2016-02-03",
            "periodTotal" : 1.5,
            "periodComment" : "comment Updated"
        })
        self.assertEqual(response.json["projectID"], 2)
        self.assertEqual(response.json["numPeriods"], 2)
        self.assertEqual(response.json["periodStart"], "2016-02-03")
        self.assertEqual(response.json["periodEnd"], "2016-02-03")
        self.assertEqual(response.json["periodTotal"], 1.5)
        self.assertEqual(response.json["periodComment"], "comment Updated")
        
    def test_delete_budget(self):
        response = self.client.delete("/api/budgets/1/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "BudgetID 1 deleted")
            
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

class TestReviewCommittee(PopulatedDB):
    def test_get_review_committees(self):
        response = self.client.get("/api/reviewcommittees/")
        self.assertEqual(response.json['reviewCommittees'][0]["project_projectID"], 1)
        self.assertEqual(response.json['reviewCommittees'][0]["RCStatusList_rc_StatusID"], 1)
        self.assertEqual(response.json['reviewCommittees'][0]["reviewCommitteeList_rcListID"], 1)
        self.assertEqual(response.json['reviewCommittees'][0]["review_committee_number"], 1)
        self.assertEqual(response.json['reviewCommittees'][0]["date_initial_review"], "2016-02-02")
        self.assertEqual(response.json['reviewCommittees'][0]["date_expires"], "2016-02-02")
        self.assertEqual(response.json['reviewCommittees'][0]["rc_note"], "rc_note")
        self.assertEqual(response.json['reviewCommittees'][0]["rc_protocol"], "rc_proto")
        self.assertEqual(response.json['reviewCommittees'][0]["rc_approval"], "rc_approval")
        
    def test_get_review_committees(self):
        response = self.client.get("/api/reviewcommittees/1/")
        self.assertEqual(response.json["project_projectID"], 1)
        self.assertEqual(response.json["RCStatusList_rc_StatusID"], 1)
        self.assertEqual(response.json["reviewCommitteeList_rcListID"], 1)
        self.assertEqual(response.json["review_committee_number"], "1")
        self.assertEqual(response.json["date_initial_review"], "2016-02-02")
        self.assertEqual(response.json["date_expires"], "2016-02-02")
        self.assertEqual(response.json["rc_note"], "rc_note")
        self.assertEqual(response.json["rc_protocol"], "rc_proto")
        self.assertEqual(response.json["rc_approval"], "rc_approval")
        
    def test_update_review_committee_list(self):
        response = self.client.put("/api/reviewcommittees/1/", data = {
            "project_projectID" : 2,
            "RCStatusList_rc_StatusID": 2,
            "reviewCommitteeList_rcListID": 2,
            "review_committee_number":"2",
            "date_initial_review":"2016-02-03",
            "date_expires" : "2016-02-03",
            "rc_note" : "rc_note Updated",
            "rc_protocol" : "rc_proto Updated",
            "rc_approval":"rc_approval Updated"
        })
        self.assertEqual(response.json["project_projectID"], 2)
        self.assertEqual(response.json["RCStatusList_rc_StatusID"], 2)
        self.assertEqual(response.json["reviewCommitteeList_rcListID"], 2)
        self.assertEqual(response.json["review_committee_number"], "2")
        self.assertEqual(response.json["date_initial_review"], "2016-02-03")
        self.assertEqual(response.json["date_expires"], "2016-02-03")
        self.assertEqual(response.json["rc_note"], "rc_note Updated")
        self.assertEqual(response.json["rc_protocol"], "rc_proto Updated")
        self.assertEqual(response.json["rc_approval"], "rc_approval Updated")
        
    def test_delete_review_committee(self):
        response = self.client.delete("/api/reviewcommittees/1/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "ReviewCommitteeID 1 deleted")
        
class TestReviewCommitteeList(PopulatedDB):
    def test_get_review_committee_lists(self):
        response = self.client.get("/api/reviewcommitteelist/")
        self.assertEqual(response.json["reviewCommitteeList"][0]["reviewCommittee"], "rc")
        self.assertEqual(response.json["reviewCommitteeList"][0]["rc_description"], "rc desc")
        
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

class TestUCRReport(PopulatedDB):
    def test_get_ucr_report(self):
        response = self.client.get("/api/ucrreports/")
        self.assertEqual(response.json["ucrReports"][0]["projectID"],1)
        self.assertEqual(response.json["ucrReports"][0]["report_type"],1)
        self.assertEqual(response.json["ucrReports"][0]["report_submitted"],"2016-02-02")
        self.assertEqual(response.json["ucrReports"][0]["report_due"],"2016-02-02")
        self.assertEqual(response.json["ucrReports"][0]["report_doc"],"doc")
        
    def test_get_ucr_report(self):
        response = self.client.get("/api/ucrreports/1/")
        self.assertEqual(response.json["projectID"],1)
        self.assertEqual(response.json["report_type"],1)
        self.assertEqual(response.json["report_submitted"],"2016-02-02")
        self.assertEqual(response.json["report_due"],"2016-02-02")
        self.assertEqual(response.json["report_doc"],"doc")
        
    def test_update_ucr_report(self):
        response = self.client.put("/api/ucrreports/1/", data = {
            "projectID" : 2,
            "report_type": 2,
            "report_submitted": "2016-02-03",
            "report_due": "2016-02-03",
            "report_doc": "doc Updated"
        })
        print(response)
        self.assertEqual(response.json["projectID"],2)
        self.assertEqual(response.json["report_type"],2)
        self.assertEqual(response.json["report_submitted"],"2016-02-03")
        self.assertEqual(response.json["report_due"],"2016-02-03")
        self.assertEqual(response.json["report_doc"],"doc Updated")
        
    def test_delete_ucr_report(self):
        response = self.client.delete("/api/ucrreports/1/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "UcrReportID 1 deleted")
        
        
        
if __name__ == '__main__':
    unittest.main()