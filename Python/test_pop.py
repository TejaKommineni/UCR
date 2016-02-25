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
        self.populate_db2()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def populate_db2(self):
        irb_holder1 = models.IRBHolderLUT(
            irb_holder = "holder 1",
            irb_holder_definition= "IRB 1")

        irb_holder2 = models.IRBHolderLUT(
            irb_holder = "holder 2",
            irb_holder_definition= "IRB 2")

        project_type1 = models.ProjectType(
            project_type = "Type 1",
            project_type_definition = "Def 1")

        project_type2 = models.ProjectType(
            project_type = "Type 2",
            project_type_definition = "Def 2")

        project1 = models.Project(
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

        project2 = models.Project(
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

        budget1 = models.Budget(
            projectID = 1,
            numPeriods = 1,
            periodStart = datetime(2016,2,2),
            periodEnd = datetime(2016,2,2),
            periodTotal = 1.23,
            periodComment = "comment")

        rcsl = models.RCStatusList(
            rc_status = "Status 1",
            rc_status_definition = "rc status def")

        rcs2 = models.RCStatusList(
            rc_status = "Status 2",
            rc_status_definition = "rc status def 2")

        rcl1 = models.ReviewCommitteeList(
            review_committee = "rc 1",
            rc_description = "rc desc 1")

        rcl2 = models.ReviewCommitteeList(
            review_committee = "rc 2",
            rc_description = "rc des 2c")

        rc = models.ReviewCommittee(
            project_projectID=1,
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
        arcReview = models.ArcReview(
            projectID = 1,
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

        grantStatus1 = models.GrantStatusLUT(
            grant_status = "status"
        )

        fundingSource1 = models.FundingSourceLUT(
            fundingSource = "source"
        )

        grantStatus2 = models.GrantStatusLUT(
            grant_status = "status2"
        )

        fundingSource2 = models.FundingSourceLUT(
            fundingSource = "source2"
        )

        funding = models.Funding(
            grantStatusLUTID = 1,
            projectID = 1,
            fundingSourceLUTID = 1,
            primary_funding_source = "pfs",
            secondary_funding_source = "sfs",
            funding_number = "number",
            grant_title = "title",
            grantStatusID = 1,
            date_status = datetime(2016,2,2),
            grant_pi = 1,
            primary_chartfield = "pcf",
            secondary_chartfield = "scf"
        )

        staff = models.Staff(
            fname = "fname",
            lname = "lname",
            middle_name = "middle_name",
            email = "email",
            phone = "phone",
            phoneComment = "phoneComment",
            institution = "institution",
            department = "department",
            position = "position",
            credentials = "credentials",
            street = "street",
            city = "city",
            state = "state",
            human_sub_training_exp = datetime(2016,2,2),
            UCR_role = 1
        )
        staff2 = models.Staff(
            fname = "fname",
            lname = "lname",
            middle_name = "middle_name",
            email = "email",
            phone = "phone",
            phoneComment = "phoneComment",
            institution = "institution",
            department = "department",
            position = "position",
            credentials = "credentials",
            street = "street",
            city = "city",
            state = "state",
            human_sub_training_exp = datetime(2016,2,2),
            UCR_role = 1
        )

        projStatusType1 = models.ProjectStatusLUT(
            project_status = "Status 1",
            status_definition = "status def"
        )
        projStatusType2 = models.ProjectStatusLUT(
            project_status = "Status 2",
            status_definition = "status def 2"
        )

        projStatus = models.ProjectStatus(
            projectStatusLUTID = 1,
            projectID = 1,
            staffID = 1,
            status_date = datetime(2016,2,2),
            status_notes = "notes"
        )

        preApp = models.PreApplication(
            projectID = 1,
            pi_fname = "pi_fname",
            pi_lname = "pi_lname",
            pi_email = "pi_email",
            pi_phone = "pi_phone",
            contact_fname = "contact_fname",
            contact_lname = "contact_lname",
            contact_phone = "contact_phone",
            contact_email = "contact_email",
            institution = "institution",
            institution2 = "institution2",
            uid = "uid",
            udoh = 1,
            project_title = "project_title",
            purpose = "purpose",
            irb0 = True,
            irb1 = True,
            irb2 = True,
            irb3 = True,
            irb4 = True,
            other_irb = "other_irb",
            updb = True,
            pt_contact = True,
            start_date = datetime(2016,2,2),
            link = True,
            delivery_date = datetime(2016,2,2),
            description = "description"
        )

        phaseStatus1 = models.PhaseStatus(
            phase_status = "status",
            phase_description = "desc"
        )

        phaseStatus2 = models.PhaseStatus(
            phase_status = "status",
            phase_description = "desc"
        )
        logSubject1 = models.LogSubjectLUT(
            log_subject = "subject"
        )
        logSubject2 = models.LogSubjectLUT(
            log_subject = "subject"
        )
        log = models.Log(
            logSubjectLUTID = 1,
            projectID = 1,
            staffID = 1,
            phaseStatusID = 1,
            note = "note",
            date = datetime(2016,2,2)
        )
        projectStaff = models.ProjectStaff(
            staffRoleLUTID = 1,
            projectID = 1,
            staffID = 1,
            role = 1,
            date_pledge = datetime(2016,2,2),
            date_revoked = datetime(2016,2,2),
            contact = "yes",
            inactive = "no",
            human_sub_training_exp = datetime(2016,2,2),
            human_sub_type_id = 1,
            study_role = 1
        )
        staffRole1 = models.StaffRoleLUT(
            staffRole = "role",
            staffRoleDescription = "desc"
        )
        staffRole2 = models.StaffRoleLUT(
            staffRole = "role",
            staffRoleDescription = "desc"
        )
        staffTraining = models.StaffTraining(
            staffID = 1,
            humanSubjectTrainingLUTID = 1,
            date_taken = datetime(2016,2,2),
            exp_date = datetime(2016,2,2)
        )
        humanSubjectTraining1 = models.HumanSubjectTrainingLUT(
            training_type = "type"
        )
        humanSubjectTraining2 = models.HumanSubjectTrainingLUT(
            training_type = "type"
        )
        patient = models.Patient(
            patID = "1",
            recordID = 1,
            ucrDistID = 1,
            UPDBID = 1,
            fname = "fname",
            lname = "lname",
            middle_name = "mname",
            maiden_name = "maiden_name",
            alias_fname = "alias_fname",
            alias_lname = "alias_lname",
            alias_middle_name = "alias_middle",
            dob = datetime(2016,2,2),
            SSN = "999999999",
            sex = "male",
            race = "white",
            ethnicity = "hispanic",
            vital_status = "v1"
        )
        patient2 = models.Patient(
            patID = "1",
            recordID = 1,
            ucrDistID = 1,
            UPDBID = 1,
            fname = "fname",
            lname = "lname",
            middle_name = "mname",
            maiden_name = "maiden_name",
            alias_fname = "alias_fname",
            alias_lname = "alias_lname",
            alias_middle_name = "alias_middle",
            dob = datetime(2016,2,2),
            SSN = "999999999",
            sex = "male",
            race = "white",
            ethnicity = "hispanic",
            vital_status = "v1"
        )

        contactInfoStatus1 = models.ContactInfoStatusLUT(
            contact_info_status = "status"
        )

        contactInfoSource1 = models.ContactInfoSourceLUT(
            contact_info_source = "source"
        )
        contactInfoStatus2 = models.ContactInfoStatusLUT(
            contact_info_status = "status"
        )

        contactInfoSource2 = models.ContactInfoSourceLUT(
            contact_info_source = "source"
        )

        patientAddress = models.PatientAddress(
            contactInfoSourceLUTID = 1,
            patientID = 1,
            contactInfoStatusLUTID = 1,
            street = "street",
            street2 = "street2",
            city = "city",
            state = "state",
            zip = "zip",
            address_status = 1,
            address_status_date = datetime(2016,2,2),
            address_status_source = "s1"
        )

        patientEmail = models.PatientEmail(
            contactInfoSourceLUTID = 1,
            patientID = 1,
            contactInfoStatusID = 1,
            email = "email",
            email_status = 1,
            email_source = 1,
            email_status_date = datetime(2016,2,2)
        )
        patientPhone = models.PatientPhone(
            contactInfoSourceLUTID = 1,
            patientID = 1,
            contactInfoStatusID = 1,
            phone = "phone",
            phone_status = 1,
            phone_source = "s1",
            phone_status_date = datetime(2016,2,2)
        )
        informant1 = models.Informant(
            patAutoID = 1,
            fname = "fname",
            lname = "lname",
            middle_name = "middle_name",
            informant_primary = "informant_primary",
            informant_relationship = "informant_relationship",
            notes = "notes"
        )
        informant2 = models.Informant(
            patAutoID = 1,
            fname = "fname",
            lname = "lname",
            middle_name = "middle_name",
            informant_primary = "informant_primary",
            informant_relationship = "informant_relationship",
            notes = "notes"
        )
        informantAddress = models.InformantAddress(
            contactInfoSourceLUTID = 1,
            informantID = 1,
            contactInfoStatusID = 1,
            street = "street",
            street2 = "street2",
            city = "city",
            state = "state",
            zip = "zip",
            address_status = 1,
            address_status_date = datetime(2016,2,2),
            address_status_source = "s1"
        )
        informantPhone = models.InformantPhone(
            contactInfoSourceLUTID = 1,
            informantID = 1,
            contactInfoStatusID = 1,
            phone = "phone",
            phone_status = 1,
            phone_source = "s1",
            phone_status_date = datetime(2016,2,2)
        )


        db.session.add(contactInfoSource1)
        db.session.add(contactInfoSource2)
        db.session.add(contactInfoStatus1)
        db.session.add(contactInfoStatus2)
        db.session.add(humanSubjectTraining1)
        db.session.add(humanSubjectTraining2)
        db.session.add(staffRole1)
        db.session.add(staffRole2)
        db.session.add(logSubject1)
        db.session.add(logSubject2)
        db.session.add(phaseStatus1)
        db.session.add(phaseStatus2)
        db.session.add(projStatusType1)
        db.session.add(projStatusType2)
        db.session.add(projStatus)
        db.session.add(staff)
        db.session.add(staff2)
        db.session.add(grantStatus1)
        db.session.add(grantStatus2)
        db.session.add(fundingSource1)
        db.session.add(fundingSource2)
        db.session.add(funding)
        db.session.add(irb_holder1)
        db.session.add(irb_holder2)
        db.session.add(project_type1)
        db.session.add(project_type2)
        db.session.add(project1)
        db.session.add(project2)
        db.session.add(budget1)
        db.session.add(rcsl)
        db.session.add(rcs2)
        db.session.add(rcl1)
        db.session.add(rcl2)
        db.session.add(rc)
        db.session.add(ucr)
        db.session.add(arcReview)
        db.session.add(preApp)
        db.session.add(log)
        db.session.add(projectStaff)
        db.session.add(staffTraining)
        db.session.add(patient)
        db.session.add(patient2)
        db.session.add(patientAddress)
        db.session.add(patientEmail)
        db.session.add(patientPhone)
        db.session.add(informant1)
        db.session.add(informant2)
        db.session.add(informantAddress)
        db.session.add(informantPhone)
        db.session.commit()

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

        irb2 = models.IRBHolderLUT(
            irb_holder = "holder 2",
            irb_holder_definition= "IRB 2")
            
        rcl = models.ReviewCommitteeList(
            review_committee = "rc",
            rc_description = "rc desc")
        
        phaseStatus = models.PhaseStatus(
            phase_status = "status",
            phase_description = "desc"
        )
        
        pt = models.ProjectType(
            project_type = "Type 1",
            project_type_definition = "Def 1")

        pt2 = models.ProjectType(
            project_type = "Type 2",
            project_type_definition = "Def 2")

        logSubject = models.LogSubjectLUT(
            log_subject = "subject"
        )
        
        log = models.Log(
            logSubjectLUTID = 1,
            projectID = 1,
            staffID = 1,
            phaseStatusID = 1,
            note = "note",
            date = datetime(2016,2,2)
        )
        projectStaff = models.ProjectStaff(
            staffRoleLUTID = 1,
            projectID = 1,
            staffID = 1,
            role = 1,
            date_pledge = datetime(2016,2,2),
            date_revoked = datetime(2016,2,2),
            contact = "yes",
            inactive = "no",
            human_sub_training_exp = datetime(2016,2,2),
            human_sub_type_id = 1,
            study_role = 1
        )
        
        rc.RCStatusList = rcsl
        rc.reviewCommitteeList = rcl
        p.irbHolder = irb
        p.projectType = pt
        p.reviewCommittees.append(rc)
        p.budgets.append(budget)
        p.arcReview = arcReview
        p.ucrReports.append(ucr)
        
        contact = models.Contact(
            contactTypeLUTID = 1,
            projectPatientID = 1,
            staffID = 1,
            informantID = 1,
            facilityID = 1,
            physicianID = 1,
            description = "desc",
            contact_date = datetime(2016,2,2),
            initials = "atp",
            notes = "notes"
        )
        
        contactType = models.ContactTypeLUT(
            contact_definition = "def"
        )
        
        contactInfoStatus = models.ContactInfoStatusLUT(
            contact_info_status = "status"
        )
        
        contactInfoSource = models.ContactInfoSourceLUT(
            contact_info_source = "source"
        )
        
        ctc = models.CTC(
            patientID = 1,
            dx_date = datetime(2016,2,2),
            site = 1,
            histology = "histology",
            behavior = "behavior",
            ctc_sequence = "sequence",
            stage = "stage",
            dx_age = 1,
            dx_street1 = "street1",
            dx_street2 = "street2",
            dx_city = "city",
            dx_state = "state",
            dx_zip = "zip",
            dx_county = "county",
            dnc = "dnc",
            dnc_reason = "dnc_reason"
        )
        
        ctcFacility = models.CTCFacility(
            ctcID = 1,
            facilityID = 1
        )
        
        facility = models.Facility(
            facility_name = "name",
            contact_fname = "fname",
            contact_lname = "lname",
            facility_status = 1,
            facility_status_date = datetime(2016,2,2),
            contact2_fname = "fname",
            contact2_lname = "lname"
        )
        
        facilityPhone = models.FacilityPhone(
            contactInfoSourceLUTID = 1,
            facilityID = 1,
            contactInfoStatusLUTID = 1,
            facility_name = "name",
            clinic_name = "clinic",
            facility_phone = "phone",
            facility_phone_status = 1,
            facility_phone_source = "s1",
            facility_phone_status_date = datetime(2016,2,2)
        )
        
        facilityAddress = models.FacilityAddress(
            contactInfoSourceLUTID = 1,
            facilityID = 1,
            contactInfoStatusLUTID = 1,
            street = "street",
            street2 = "street2",
            city = "city",
            state = "state",
            zip = "zip",
            address_status = 1,
            address_status_date = datetime(2016,2,2),
            address_status_source = "s1"
        )
        
        funding = models.Funding(
            grantStatusLUTID = 1,
            projectID = 1,
            fundingSourceLUTID = 1,
            primary_funding_source = "pfs",
            secondary_funding_source = "sfs",
            funding_number = "number",
            grant_title = "title",
            grantStatusID = 1,
            date_status = datetime(2016,2,2),
            grant_pi = 1,
            primary_chartfield = "pcf",
            secondary_chartfield = "scf"
        )
        
        fundingSourceLUT = models.FundingSourceLUT(
            fundingSource = "fs"
        )
        
        humanSubjectTraining = models.HumanSubjectTrainingLUT(
            training_type = "type"
        )
        
        informant = models.Informant(
            patAutoID = 1,
            fname = "fname",
            lname = "lname",
            middle_name = "middle_name",
            informant_primary = "informant_primary",
            informant_relationship = "informant_relationship",
            notes = "notes"
        )
        
        informantAddress = models.InformantAddress(
            contactInfoSourceLUTID = 1,
            informantID = 1,
            contactInfoStatusID = 1,
            street = "street",
            street2 = "street2",
            city = "city",
            state = "state",
            zip = "zip",
            address_status = 1,
            address_status_date = datetime(2016,2,2),
            address_status_source = "s1"
        )
        
        informantPhone = models.InformantPhone(
            contactInfoSourceLUTID = 1,
            informantID = 1,
            contactInfoStatusID = 1,
            phone = "phone",
            phone_status = 1,
            phone_source = "s1",
            phone_status_date = datetime(2016,2,2)
        )
        
        grantStatus = models.GrantStatusLUT(
            grant_status = "status"
        )
        
        patient = models.Patient(
            patID = "1",
            recordID = 1,
            ucrDistID = 1,
            UPDBID = 1,
            fname = "fname",
            lname = "lname",
            middle_name = "mname",
            maiden_name = "maiden_name",
            alias_fname = "alias_fname",
            alias_lname = "alias_lname",
            alias_middle_name = "alias_middle",
            dob = datetime(2016,2,2),
            SSN = "999999999",
            sex = "male",
            race = "white",
            ethnicity = "hispanic",
            vital_status = "v1"
        )
        
        patientAddress = models.PatientAddress(
            contactInfoSourceLUTID = 1,
            patientID = 1,
            contactInfoStatusLUTID = 1,
            street = "street",
            street2 = "street2",
            city = "city",
            state = "state",
            zip = "zip",
            address_status = 1,
            address_status_date = datetime(2016,2,2),
            address_status_source = "s1"
        )
        
        patientEmail = models.PatientEmail(
            contactInfoSourceLUTID = 1,
            patientID = 1,
            contactInfoStatusID = 1,
            email = "email",
            email_status = 1,
            email_source = 1,
            email_status_date = datetime(2016,2,2)
        )
        
        patientPhone = models.PatientPhone(
            contactInfoSourceLUTID = 1,
            patientID = 1,
            contactInfoStatusID = 1,
            phone = "phone",
            phone_status = 1,
            phone_source = "s1",
            phone_status_date = datetime(2016,2,2)
        )
        
        patientProjectStatus = models.PatientProjectStatus(
            patientProjectStatusLUTID =1,
            projectPatientID = 1,
        )
        
        patientProjectStatusType = models.PatientProjectStatusLUT(
            status_description = "desc"
        )
        
        physician = models.Physician(
            fname = "fname",
            lname = "lname",
            middle_name = "middle_name",
            credentials = "credentials",
            specialty = "specialty",
            alias_fname = "alias_fname",
            alias_lname = "alias_lname",
            alias_middle_name = "alias_middle_name",
            physician_status = 1,
            physician_status_date = datetime(2016,2,2),
            email = "email"
        )
        
        physicianAddress = models.PhysicianAddress(
            contactInfoSourceLUTID = 1,
            physicianID = 1,
            contactInfoStatusLUTID = 1,
            street = "street",
            street2 = "street2",
            city = "city",
            state = "state",
            zip = "zip",
            address_status = 1,
            address_status_date = datetime(2016,2,2),
            address_status_source = "s1"
        )
        
        physicianFacility = models.PhysicianFacility(
            facilityID = 1,
            physicianID = 1,
            phys_facility_status = "s1",
            phys_facility_status_date = datetime(2016,2,2)
        )
        
        physicianPhone = models.PhysicianPhone(
            contactInfoSourceLUTID = 1,
            physicianID = 1,
            contactInfoStatusID = 1,
            phone = "phone",
            phone_type = "phone_type",
            phone_status = 1,
            phone_source = "s1",
            phone_status_date = datetime(2016,2,2)
        )
        
        physicianToCTC = models.PhysicianToCTC(
            physicianID = 1,
            ctcID = 1
        )
        
        preApp = models.PreApplication(
            projectID = 1,
            pi_fname = "pi_fname",
            pi_lname = "pi_lname",
            pi_email = "pi_email",
            pi_phone = "pi_phone",
            contact_fname = "contact_fname",
            contact_lname = "contact_lname",
            contact_phone = "contact_phone",
            contact_email = "contact_email",
            institution = "institution",
            institution2 = "institution2",
            uid = "uid",
            udoh = 1,
            project_title = "project_title",
            purpose = "purpose",
            irb0 = True,
            irb1 = True,
            irb2 = True,
            irb3 = True,
            irb4 = True,
            other_irb = "other_irb",
            updb = True,
            pt_contact = True,
            start_date = datetime(2016,2,2),
            link = True,
            delivery_date = datetime(2016,2,2),
            description = "description"
        )
        
        projStatus = models.ProjectStatus(
            projectStatusLUTID = 1,
            projectID = 1,
            staffID = 1,
            status_date = datetime(2016,2,2),
            status_notes = "notes"
        
        )
        
        projStatusType = models.ProjectStatusLUT(
            project_status = "Status 1",
            status_definition = "status def",)
            
        projectPatient = models.ProjectPatient(
            projectID = 1,
            staffID = 1,
            ctcID = 1,
            current_age = 1,
            batch = 1,
            sitegrp = 1,
            final_code = 1,
            final_code_date = datetime(2016,2,2),
            enrollment_date = datetime(2016,2,2),
            date_coord_signed = datetime(2016,2,2),
            import_date = datetime(2016,2,2),
            final_code_staff = 1,
            enrollment_staff = 1,
            date_coord_signed_staff = datetime(2016,2,2),
            abstract_status = 1,
            abstract_status_date = datetime(2016,2,2),
            abstract_status_staff = 1,
            sent_to_abstractor = datetime(2016,2,2),
            sent_to_abstractor_staff = 1,
            abstracted_date = datetime(2016,2,2),
            abstractor_initials = "atp",
            researcher_date = datetime(2016,2,2),
            researcher_staff = 1,
            consent_link = "link",
            tracing_status = 1,
            med_record_release_signed = True,
            med_record_release_link = "link",
            med_record_release_staff = 1,
            med_record_release_date = datetime(2016,2,2),
            survey_to_researcher = datetime(2016,2,2),
            survey_to_researcher_staff = 1
        )
        staff = models.Staff(
            fname = "fname",
            lname = "lname",
            middle_name = "middle_name",
            email = "email",
            phone = "phone",
            phoneComment = "phoneComment",
            institution = "institution",
            department = "department",
            position = "position",
            credentials = "credentials",
            street = "street",
            city = "city",
            state = "state",
            human_sub_training_exp = datetime(2016,2,2),
            UCR_role = 1
        )
        
        staffRole = models.StaffRoleLUT(
            staffRole = "role",
            staffRoleDescription = "desc"
        )
        staffTraining = models.StaffTraining(
            staffID = 1,
            humanSubjectTrainingLUTID = 1,
            date_taken = datetime(2016,2,2),
            exp_date = datetime(2016,2,2)
        )
        
        tracing = models.Tracing(
            tracingSourceLUTID = 1,
            projectPatientID = 1,
            date = datetime(2016,2,2),
            staff = 1,
            notes = "notes"
        )
        tracingSource = models.TracingSourceLUT(
            description = "desc"
        )
        db.session.add(facilityAddress)
        db.session.add(physicianFacility)
        db.session.add(physicianPhone)
        db.session.add(physicianAddress)
        db.session.add(physician)
        db.session.add(ctcFacility)
        db.session.add(facility)
        db.session.add(physicianToCTC)
        db.session.add(humanSubjectTraining)
        db.session.add(staffRole)
        db.session.add(staffTraining)
        db.session.add(staff)
        db.session.add(ctc)
        db.session.add(contact)
        db.session.add(contactType)
        db.session.add(facilityPhone)
        db.session.add(contactInfoSource)
        db.session.add(contactInfoStatus)
        db.session.add(patientProjectStatusType)
        db.session.add(patientProjectStatus)
        db.session.add(tracing)
        db.session.add(tracingSource)
        db.session.add(informant)
        db.session.add(informantAddress)
        db.session.add(informantPhone)
        db.session.add(patientPhone)
        db.session.add(patientEmail)
        db.session.add(patientAddress)
        db.session.add(preApp)
        db.session.add(projectStaff)
        db.session.add(log)
        db.session.add(logSubject)
        db.session.add(phaseStatus)
        db.session.add(patient)
        db.session.add(projectPatient)
        db.session.add(projStatusType)
        db.session.add(funding)
        db.session.add(fundingSourceLUT)
        db.session.add(grantStatus)
        db.session.add(projStatus)
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

class TestContact(PopulatedDB):
    def test_get_contacts(self):
        response = self.client.get("/api/contacts/")
        self.assertEqual(response.json["Contacts"][0]["contactID"], 1)
        self.assertEqual(response.json["Contacts"][0]["contactTypeLUTID"], 1)
        self.assertEqual(response.json["Contacts"][0]["projectPatientID"], 1)
        self.assertEqual(response.json["Contacts"][0]["staffID"], 1)
        self.assertEqual(response.json["Contacts"][0]["informantID"], 1)
        self.assertEqual(response.json["Contacts"][0]["facilityID"], 1)
        self.assertEqual(response.json["Contacts"][0]["physicianID"], 1)
        self.assertEqual(response.json["Contacts"][0]["description"], "desc")
        self.assertEqual(response.json["Contacts"][0]["contact_date"], "2016-02-02")
        self.assertEqual(response.json["Contacts"][0]["initials"], "atp")
        self.assertEqual(response.json["Contacts"][0]["notes"], "notes")
        
    def test_get_contact(self):
        response = self.client.get("/api/contacts/1/")
        self.assertEqual(response.json["contactID"], 1)
        self.assertEqual(response.json["contactTypeLUTID"], 1)
        self.assertEqual(response.json["projectPatientID"], 1)
        self.assertEqual(response.json["staffID"], 1)
        self.assertEqual(response.json["informantID"], 1)
        self.assertEqual(response.json["facilityID"], 1)
        self.assertEqual(response.json["physicianID"], 1)
        self.assertEqual(response.json["description"], "desc")
        self.assertEqual(response.json["contact_date"], "2016-02-02")
        self.assertEqual(response.json["initials"], "atp")
        self.assertEqual(response.json["notes"], "notes")
        
    def test_update_contact(self):
        response = self.client.put("/api/contacts/1/",data = {
            "contactTypeLUTID" : 2,
            "projectPatientID" : 2,
            "staffID" : 2,
            "informantID" : 2,
            "facilityID" : 2,
            "physicianID" : 2,
            "description" : "desc Updated",
            "contact_date" : "2016-02-03",
            "initials" : "atp Updated",
            "notes" : "notes Updated"
        })
        self.assertEqual(response.json["contactID"], 1)
        self.assertEqual(response.json["contactTypeLUTID"], 2)
        self.assertEqual(response.json["projectPatientID"], 2)
        self.assertEqual(response.json["staffID"], 2)
        self.assertEqual(response.json["informantID"], 2)
        self.assertEqual(response.json["facilityID"], 2)
        self.assertEqual(response.json["physicianID"], 2)
        self.assertEqual(response.json["description"], "desc Updated")
        self.assertEqual(response.json["contact_date"], "2016-02-03")
        self.assertEqual(response.json["initials"], "atp Updated")
        self.assertEqual(response.json["notes"], "notes Updated")
        
    def test_delete_contact(self):
        response = self.client.delete("/api/contacts/1/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "ContactID 1 deleted")  
        
class TestContactType(PopulatedDB):
    def test_get_contact_types(self):
        response = self.client.get("/api/contacttypes/")
        self.assertEqual(response.json["ContactTypes"][0]["contactTypeLUTID"], 1)
        self.assertEqual(response.json["ContactTypes"][0]["contact_definition"], "def")
        
    def test_get_contact_type(self):
        response = self.client.get("/api/contacttypes/1/")
        self.assertEqual(response.json["contactTypeLUTID"], 1)
        self.assertEqual(response.json["contact_definition"], "def")
        
    def test_update_contact_type(self):
        response = self.client.put("/api/contacttypes/1/",data = {
            "contact_definition" : "def Updated",
        })
        self.assertEqual(response.json["contactTypeLUTID"], 1)
        self.assertEqual(response.json["contact_definition"], "def Updated")
        
    def test_delete_contact_type(self):
        response = self.client.delete("/api/contacttypes/1/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "ContactTypeLUTID 1 deleted")        
        
class TestContactInfoSource(PopulatedDB):
    def test_get_contact_info_sourcees(self):
        response = self.client.get("/api/contactinfosources/")
        self.assertEqual(response.json["ContactInfoSources"][0]["contactInfoSourceLUTID"], 1)
        self.assertEqual(response.json["ContactInfoSources"][0]["contact_info_source"], "source")
        
    def test_get_contact_info_source(self):
        response = self.client.get("/api/contactinfosources/1/")
        self.assertEqual(response.json["contactInfoSourceLUTID"], 1)
        self.assertEqual(response.json["contact_info_source"], "source")
        
    def test_update_contact_info_source(self):
        response = self.client.put("/api/contactinfosources/1/",data = {
            "contact_info_source" : "source",
        })
        print(response.json)
        self.assertEqual(response.json["contactInfoSourceLUTID"], 1)
        self.assertEqual(response.json["contact_info_source"], "source Updated")
        
    def test_delete_contact_info_source(self):
        response = self.client.delete("/api/contactinfosources/1/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "ContactInfoSourceLUTID 1 deleted")        
        
class TestContactInfoStatus(PopulatedDB):
    def test_get_contact_info_statuses(self):
        response = self.client.get("/api/contactinfostatuses/")
        self.assertEqual(response.json["ContactInfoStatuses"][0]["contactInfoStatusID"], 1)
        self.assertEqual(response.json["ContactInfoStatuses"][0]["contact_info_status"], "status")
        
    def test_get_contact_info_status(self):
        response = self.client.get("/api/contactinfostatuses/1/")
        self.assertEqual(response.json["contactInfoStatusID"], 1)
        self.assertEqual(response.json["contact_info_status"], "status")
        
    def test_update_contact_info_status(self):
        response = self.client.put("/api/contactinfostatuses/1/",data = {
            "contact_info_status" : "status Updated",
        })
        self.assertEqual(response.json["contactInfoStatusID"], 1)
        self.assertEqual(response.json["contact_info_status"], "status Updated")
        
    def test_delete_contact_info_status(self):
        response = self.client.delete("/api/contactinfostatuses/1/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "ContactInfoStatusID 1 deleted")

class TestCTC(PopulatedDB):
    def test_get_ctcs(self):
        response = self.client.get("/api/ctcs/")
        self.assertEqual(response.json["CTCs"][0]["ctcID"], 1)
        self.assertEqual(response.json["CTCs"][0]["patientID"], 1)
        self.assertEqual(response.json["CTCs"][0]["dx_date"], "2016-02-02")
        self.assertEqual(response.json["CTCs"][0]["site"], 1)
        self.assertEqual(response.json["CTCs"][0]["histology"], "histology")
        self.assertEqual(response.json["CTCs"][0]["behavior"], "behavior")
        self.assertEqual(response.json["CTCs"][0]["ctc_sequence"], "sequence")
        self.assertEqual(response.json["CTCs"][0]["stage"], "stage")
        self.assertEqual(response.json["CTCs"][0]["dx_age"], 1)
        self.assertEqual(response.json["CTCs"][0]["dx_street1"], "street1")
        self.assertEqual(response.json["CTCs"][0]["dx_street2"], "street2")
        self.assertEqual(response.json["CTCs"][0]["dx_city"], "city")
        self.assertEqual(response.json["CTCs"][0]["dx_state"], "state")
        self.assertEqual(response.json["CTCs"][0]["dx_zip"], "zip")
        self.assertEqual(response.json["CTCs"][0]["dx_county"], "county")
        self.assertEqual(response.json["CTCs"][0]["dnc"], "dnc")
        self.assertEqual(response.json["CTCs"][0]["dnc_reason"], "dnc_reason")
        
    def test_get_ctc(self):
        response = self.client.get("/api/ctcs/1/")
        self.assertEqual(response.json["ctcID"], 1)
        self.assertEqual(response.json["patientID"], 1)
        self.assertEqual(response.json["dx_date"], "2016-02-02")
        self.assertEqual(response.json["site"], 1)
        self.assertEqual(response.json["histology"], "histology")
        self.assertEqual(response.json["behavior"], "behavior")
        self.assertEqual(response.json["ctc_sequence"], "sequence")
        self.assertEqual(response.json["stage"], "stage")
        self.assertEqual(response.json["dx_age"], 1)
        self.assertEqual(response.json["dx_street1"], "street1")
        self.assertEqual(response.json["dx_street2"], "street2")
        self.assertEqual(response.json["dx_city"], "city")
        self.assertEqual(response.json["dx_state"], "state")
        self.assertEqual(response.json["dx_zip"], "zip")
        self.assertEqual(response.json["dx_county"], "county")
        self.assertEqual(response.json["dnc"], "dnc")
        self.assertEqual(response.json["dnc_reason"], "dnc_reason")
        
    def test_update_ctc(self):
        response = self.client.put("/api/ctcs/1/",data = {
            "patientID" : 2,
            "dx_date" : "2016-02-03",
            "site" : 2,
            "histology" : "histology2",
            "behavior" : "behavior2",
            "ctc_sequence" : "sequence2",
            "stage" : "stage2",
            "dx_age" : 2,
            "dx_street1" : "street12",
            "dx_street2" : "street22",
            "dx_city" : "city2",
            "dx_state" : "state2",
            "dx_zip" : "zip2",
            "dx_county" : "county2",
            "dnc" : "dnc2",
            "dnc_reason" : "dnc_reason2"
        })
        self.assertEqual(response.json["ctcID"], 1)
        self.assertEqual(response.json["patientID"], 2)
        self.assertEqual(response.json["dx_date"], "2016-02-03")
        self.assertEqual(response.json["site"], 2)
        self.assertEqual(response.json["histology"], "histology2")
        self.assertEqual(response.json["behavior"], "behavior2")
        self.assertEqual(response.json["ctc_sequence"], "sequence2")
        self.assertEqual(response.json["stage"], "stage2")
        self.assertEqual(response.json["dx_age"], 2)
        self.assertEqual(response.json["dx_street1"], "street12")
        self.assertEqual(response.json["dx_street2"], "street22")
        self.assertEqual(response.json["dx_city"], "city2")
        self.assertEqual(response.json["dx_state"], "state2")
        self.assertEqual(response.json["dx_zip"], "zip2")
        self.assertEqual(response.json["dx_county"], "county2")
        self.assertEqual(response.json["dnc"], "dnc2")
        self.assertEqual(response.json["dnc_reason"], "dnc_reason2")
        
    def test_delete_ctc(self):
        response = self.client.delete("/api/ctcs/1/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "CtcID 1 deleted")

class TestCTCFacility(PopulatedDB):
    def test_get_ctc_facilities(self):
        response = self.client.get("/api/ctcfacilities/")
        self.assertEqual(response.json["CTCFacilities"][0]["CTCFacilityID"], 1)
        self.assertEqual(response.json["CTCFacilities"][0]["ctcID"], 1)
        self.assertEqual(response.json["CTCFacilities"][0]["facilityID"], 1)
        
    def test_get_ctc_facility(self):
        response = self.client.get("/api/ctcfacilities/1/")
        self.assertEqual(response.json["CTCFacilityID"], 1)
        self.assertEqual(response.json["ctcID"], 1)
        self.assertEqual(response.json["facilityID"], 1)
        
    def test_update_ctc_facility(self):
        response = self.client.put("/api/ctcfacilities/1/",data = {
            "ctcID" : 2,
            "facilityID" : 2
        })
        self.assertEqual(response.json["CTCFacilityID"], 1)
        self.assertEqual(response.json["ctcID"], 2)
        self.assertEqual(response.json["facilityID"], 2)
        
    def test_delete_ctc_facility(self):
        response = self.client.delete("/api/ctcfacilities/1/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "CTCFacilityID 1 deleted")
             
class TestFacilityPhone(PopulatedDB):
    def test_get_facility_phones(self):
        response = self.client.get("/api/facilityphones/")
        self.assertEqual(response.json["FacilityPhones"][0]["facilityPhoneID"], 1)
        self.assertEqual(response.json["FacilityPhones"][0]["contactInfoSourceLUTID"], 1)
        self.assertEqual(response.json["FacilityPhones"][0]["facilityID"], 1)
        self.assertEqual(response.json["FacilityPhones"][0]["contactInfoStatusLUTID"], 1)
        self.assertEqual(response.json["FacilityPhones"][0]["facility_name"], "name")
        self.assertEqual(response.json["FacilityPhones"][0]["clinic_name"], "clinic")
        self.assertEqual(response.json["FacilityPhones"][0]["facility_phone"], "phone")
        self.assertEqual(response.json["FacilityPhones"][0]["facility_phone_status"], 1)
        self.assertEqual(response.json["FacilityPhones"][0]["facility_phone_source"], "s1")
        self.assertEqual(response.json["FacilityPhones"][0]["facility_phone_status_date"], "2016-02-02")
        
    def test_get_facility_phone(self):
        response = self.client.get("/api/facilityphones/1/")
        self.assertEqual(response.json["facilityPhoneID"], 1)
        self.assertEqual(response.json["contactInfoSourceLUTID"], 1)
        self.assertEqual(response.json["facilityID"], 1)
        self.assertEqual(response.json["contactInfoStatusLUTID"], 1)
        self.assertEqual(response.json["facility_name"], "name")
        self.assertEqual(response.json["clinic_name"], "clinic")
        self.assertEqual(response.json["facility_phone"], "phone")
        self.assertEqual(response.json["facility_phone_status"], 1)
        self.assertEqual(response.json["facility_phone_source"], "s1")
        self.assertEqual(response.json["facility_phone_status_date"], "2016-02-02")
        
    def test_update_facility_phone(self):
        response = self.client.put("/api/facilityphones/1/", data = {
            "contactInfoSourceLUTID" : 2,
            "facilityID" : 2,
            "contactInfoStatusLUTID" : 2,
            "facility_name" : "name Updated",
            "clinic_name" : "clinic Updated",
            "facility_phone" : "phone Updated",
            "facility_phone_status" : 2,
            "facility_phone_source" : "s2",
            "facility_phone_status_date" : "2016-02-03"
        })
        self.assertEqual(response.json["facilityPhoneID"], 1)
        self.assertEqual(response.json["contactInfoSourceLUTID"], 2)
        self.assertEqual(response.json["facilityID"], 2)
        self.assertEqual(response.json["contactInfoStatusLUTID"], 2)
        self.assertEqual(response.json["facility_name"], "name Updated")
        self.assertEqual(response.json["clinic_name"], "clinic Updated")
        self.assertEqual(response.json["facility_phone"], "phone Updated")
        self.assertEqual(response.json["facility_phone_status"], 2)
        self.assertEqual(response.json["facility_phone_source"], "s2")
        self.assertEqual(response.json["facility_phone_status_date"], "2016-02-03")

    def test_delete_facility_phone(self):
        response = self.client.delete("/api/facilityphones/1/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "FacilityPhoneID 1 deleted")      

class TestFacility(PopulatedDB):
    def test_get_facilities(self):
        response = self.client.get("/api/facilities/")
        self.assertEqual(response.json["Facilities"][0]["facility_name"], "name")
        self.assertEqual(response.json["Facilities"][0]["contact_fname"], "fname")
        self.assertEqual(response.json["Facilities"][0]["contact_lname"], "lname")
        self.assertEqual(response.json["Facilities"][0]["facility_status"], 1)
        self.assertEqual(response.json["Facilities"][0]["facility_status_date"], "2016-02-02")
        self.assertEqual(response.json["Facilities"][0]["contact2_fname"], "fname")
        self.assertEqual(response.json["Facilities"][0]["contact2_lname"], "lname")

    def test_get_facility(self):
        response = self.client.get("/api/facilities/1/")
        self.assertEqual(response.json["facility_name"], "name")
        self.assertEqual(response.json["contact_fname"], "fname")
        self.assertEqual(response.json["contact_lname"], "lname")
        self.assertEqual(response.json["facility_status"], 1)
        self.assertEqual(response.json["facility_status_date"], "2016-02-02")
        self.assertEqual(response.json["contact2_fname"], "fname")
        self.assertEqual(response.json["contact2_lname"], "lname")
        
    def test_update_facility(self):
        response = self.client.put("/api/facilities/1/", data = {
            "facility_name" : "name2",
            "contact_fname" : "fname2",
            "contact_lname" : "lname2",
            "facility_status" : 2,
            "facility_status_date" : "2016-02-03",
            "contact2_fname" : "fname2",
            "contact2_lname" : "lname2"
        })
        self.assertEqual(response.json["facility_name"], "name2")
        self.assertEqual(response.json["contact_fname"], "fname2")
        self.assertEqual(response.json["contact_lname"], "lname2")
        self.assertEqual(response.json["facility_status"], 2)
        self.assertEqual(response.json["facility_status_date"], "2016-02-03")
        self.assertEqual(response.json["contact2_fname"], "fname2")
        self.assertEqual(response.json["contact2_lname"], "lname2")

    def test_delete_facility(self):
        response = self.client.delete("/api/facilities/1/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "FacilityID 1 deleted")      

class TestFacilityAddress(PopulatedDB):
    def test_get_facility_addresses(self):
        response = self.client.get("/api/facilityaddresses/")
        self.assertEqual(response.json["FacilityAddresses"][0]["facilityAddressID"], 1)
        self.assertEqual(response.json["FacilityAddresses"][0]["contactInfoSourceLUTID"], 1)
        self.assertEqual(response.json["FacilityAddresses"][0]["facilityID"], 1)
        self.assertEqual(response.json["FacilityAddresses"][0]["contactInfoStatusLUTID"], 1)
        self.assertEqual(response.json["FacilityAddresses"][0]["street"], "street")
        self.assertEqual(response.json["FacilityAddresses"][0]["street2"], "street2")
        self.assertEqual(response.json["FacilityAddresses"][0]["city"], "city")
        self.assertEqual(response.json["FacilityAddresses"][0]["state"], "state")
        self.assertEqual(response.json["FacilityAddresses"][0]["zip"], "zip")
        self.assertEqual(response.json["FacilityAddresses"][0]["address_status"], 1)
        self.assertEqual(response.json["FacilityAddresses"][0]["address_status_date"], "2016-02-02")
        self.assertEqual(response.json["FacilityAddresses"][0]["address_status_source"], "s1")
        
    def test_get_facility_address(self):
        response = self.client.get("/api/facilityaddresses/1/")
        self.assertEqual(response.json["facilityAddressID"], 1)
        self.assertEqual(response.json["contactInfoSourceLUTID"], 1)
        self.assertEqual(response.json["facilityID"], 1)
        self.assertEqual(response.json["contactInfoStatusLUTID"], 1)
        self.assertEqual(response.json["street"], "street")
        self.assertEqual(response.json["street2"], "street2")
        self.assertEqual(response.json["city"], "city")
        self.assertEqual(response.json["state"], "state")
        self.assertEqual(response.json["zip"], "zip")
        self.assertEqual(response.json["address_status"], 1)
        self.assertEqual(response.json["address_status_date"], "2016-02-02")
        self.assertEqual(response.json["address_status_source"], "s1")
        
    def test_update_facility_address(self):
        response = self.client.put("/api/facilityaddresses/1/", data = {
            "contactInfoSourceLUTID" : 2,
            "facilityID" : 2,
            "contactInfoStatusLUTID" : 2,
            "street" : "street Updated",
            "street2" : "street2 Updated",
            "city" : "city Updated",
            "state" : "state Updated",
            "zip" : "zip Updated",
            "address_status" : 2,
            "address_status_date" : "2016-02-03",
            "address_status_source" : "s2"
        })
        self.assertEqual(response.json["facilityAddressID"], 1)
        self.assertEqual(response.json["contactInfoSourceLUTID"], 2)
        self.assertEqual(response.json["facilityID"], 2)
        self.assertEqual(response.json["contactInfoStatusLUTID"], 2)
        self.assertEqual(response.json["street"], "street Updated")
        self.assertEqual(response.json["street2"], "street2 Updated")
        self.assertEqual(response.json["city"], "city Updated")
        self.assertEqual(response.json["state"], "state Updated")
        self.assertEqual(response.json["zip"], "zip Updated")
        self.assertEqual(response.json["address_status"], 2)
        self.assertEqual(response.json["address_status_date"], "2016-02-03")
        self.assertEqual(response.json["address_status_source"], "s2")
        
    def test_delete_facility_address(self):
        response = self.client.delete("/api/facilityaddresses/1/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "FacilityAddressID 1 deleted")       
        
class TestFunding(PopulatedDB):
    def test_get_fundings(self):
        response = self.client.get("/api/fundings/")
        self.assertEqual(response.json["Fundings"][0]["fundingID"], 1)
        self.assertEqual(response.json["Fundings"][0]["grantStatusLUTID"], 1)
        self.assertEqual(response.json["Fundings"][0]["projectID"], 1)
        self.assertEqual(response.json["Fundings"][0]["fundingSourceLUTID"], 1)
        self.assertEqual(response.json["Fundings"][0]["primary_funding_source"], "pfs")
        self.assertEqual(response.json["Fundings"][0]["secondary_funding_source"], "sfs")
        self.assertEqual(response.json["Fundings"][0]["funding_number"], "number")
        self.assertEqual(response.json["Fundings"][0]["grant_title"], "title")
        self.assertEqual(response.json["Fundings"][0]["grantStatusID"], 1)
        self.assertEqual(response.json["Fundings"][0]["date_status"], "2016-02-02")
        self.assertEqual(response.json["Fundings"][0]["grant_pi"], 1)
        self.assertEqual(response.json["Fundings"][0]["primary_chartfield"], "pcf")
        self.assertEqual(response.json["Fundings"][0]["secondary_chartfield"], "scf")

    def test_get_funding(self):
        response = self.client.get("/api/fundings/1/")
        self.assertEqual(response.json["fundingID"], 1)
        self.assertEqual(response.json["grantStatusLUTID"], 1)
        self.assertEqual(response.json["projectID"], 1)
        self.assertEqual(response.json["fundingSourceLUTID"], 1)
        self.assertEqual(response.json["primary_funding_source"], "pfs")
        self.assertEqual(response.json["secondary_funding_source"], "sfs")
        self.assertEqual(response.json["funding_number"], "number")
        self.assertEqual(response.json["grant_title"], "title")
        self.assertEqual(response.json["grantStatusID"], 1)
        self.assertEqual(response.json["date_status"], "2016-02-02")
        self.assertEqual(response.json["grant_pi"], 1)
        self.assertEqual(response.json["primary_chartfield"], "pcf")
        self.assertEqual(response.json["secondary_chartfield"], "scf")
        
    def test_update_funding(self):
        response = self.client.put("/api/fundings/1/", data = {
            "fundingID": 1,
            "grantStatusLUTID": 2,
            "projectID": 2,
            "fundingSourceLUTID": 2,
            "primary_funding_source": "pfs Updated",
            "secondary_funding_source": "sfs Updated",
            "funding_number": "number Updated",
            "grant_title": "title Updated",
            "grantStatusID": 2,
            "date_status": "2016-02-03",
            "grant_pi": 2,
            "primary_chartfield": "pcf Updated",
            "secondary_chartfield": "scf Updated"
        })
        self.assertEqual(response.json["fundingID"], 1)
        self.assertEqual(response.json["grantStatusLUTID"], 2)
        self.assertEqual(response.json["projectID"], 2)
        self.assertEqual(response.json["fundingSourceLUTID"], 2)
        self.assertEqual(response.json["primary_funding_source"], "pfs Updated")
        self.assertEqual(response.json["secondary_funding_source"], "sfs Updated")
        self.assertEqual(response.json["funding_number"], "number Updated")
        self.assertEqual(response.json["grant_title"], "title Updated")
        self.assertEqual(response.json["grantStatusID"], 2)
        self.assertEqual(response.json["date_status"], "2016-02-03")
        self.assertEqual(response.json["grant_pi"], 2)
        self.assertEqual(response.json["primary_chartfield"], "pcf Updated")
        self.assertEqual(response.json["secondary_chartfield"], "scf Updated")
        
    def test_delete_funding(self):
        response = self.client.delete("/api/fundings/1/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "FundingID 1 deleted")  
        
class TestFundingSource(PopulatedDB):
    def test_get_funding_sources(self):
        response = self.client.get("/api/fundingsources/")
        self.assertEqual(response.json["FundingSources"][0]["fundingSourceLUTID"], 1)
        self.assertEqual(response.json["FundingSources"][0]["fundingSource"], "source")

    def test_get_funding_source(self):
        response = self.client.get("/api/fundingsources/1/")
        self.assertEqual(response.json["fundingSourceLUTID"], 1)
        self.assertEqual(response.json["fundingSource"], "source")
        
    def test_update_funding_source(self):
        response = self.client.put("/api/fundingsources/1/", data = {
            "fundingSource" : "source2",
        })
        self.assertEqual(response.json["fundingSource"], "source2")
        
    def test_delete_funding_source(self):
        response = self.client.delete("/api/fundingsources/1/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "FundingSourceLUTID 1 deleted")             
        
class TestGrantStatus(PopulatedDB):
    def test_get_grant_statuses(self):
        response = self.client.get("/api/grantstatuses/")
        self.assertEqual(response.json["GrantStatuses"][0]["grantStatusLUTID"], 1)
        self.assertEqual(response.json["GrantStatuses"][0]["grant_status"], "status")

    def test_get_grant_status(self):
        response = self.client.get("/api/grantstatuses/1/")
        self.assertEqual(response.json["grantStatusLUTID"], 1)
        self.assertEqual(response.json["grant_status"], "status")
        
    def test_update_grant_status(self):
        response = self.client.put("/api/grantstatuses/1/", data = {
            "grant_status" : "status2"
        })
        self.assertEqual(response.json["grant_status"], "status2")
        
    def test_delete_grant_status(self):
        response = self.client.delete("/api/grantstatuses/1/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "GrantStatusLUTID 1 deleted")     

class TestHumanSubjectTraining(PopulatedDB):
    def test_get_human_subject_trainings(self):
        response = self.client.get("/api/humansubjecttrainings/")
        self.assertEqual(response.json["HumanSubjectTrainings"][0]["humanSubjectTrainingID"], 1)
        self.assertEqual(response.json["HumanSubjectTrainings"][0]["training_type"], "type")

    def test_get_human_subject_training(self):
        response = self.client.get("/api/humansubjecttrainings/1/")
        self.assertEqual(response.json["humanSubjectTrainingID"], 1)
        self.assertEqual(response.json["training_type"], "type")
        
    def test_update_human_subject_training(self):
        response = self.client.put("/api/humansubjecttrainings/1/", data = {
            "training_type" : "type Updated",
        })
        self.assertEqual(response.json["training_type"], "type Updated")
        
    def test_delete_human_subject_training(self):
        response = self.client.delete("/api/humansubjecttrainings/1/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "HumanSubjectTrainingID 1 deleted")     

class TestInformant(PopulatedDB):
    def test_get_informants(self):
        response = self.client.get("/api/informants/")
        self.assertEqual(response.json["Informants"][0]["informantID"], 1)
        self.assertEqual(response.json["Informants"][0]["patAutoID"], 1)
        self.assertEqual(response.json["Informants"][0]["fname"], "fname")
        self.assertEqual(response.json["Informants"][0]["lname"], "lname")
        self.assertEqual(response.json["Informants"][0]["middle_name"], "middle_name")
        self.assertEqual(response.json["Informants"][0]["informant_primary"], "informant_primary")
        self.assertEqual(response.json["Informants"][0]["informant_relationship"], "informant_relationship")
        self.assertEqual(response.json["Informants"][0]["notes"], "notes")
        
    def test_get_informant(self):
        response = self.client.get("/api/informants/1/")
        self.assertEqual(response.json["informantID"], 1)
        self.assertEqual(response.json["patAutoID"], 1)
        self.assertEqual(response.json["fname"], "fname")
        self.assertEqual(response.json["lname"], "lname")
        self.assertEqual(response.json["middle_name"], "middle_name")
        self.assertEqual(response.json["informant_primary"], "informant_primary")
        self.assertEqual(response.json["informant_relationship"], "informant_relationship")
        self.assertEqual(response.json["notes"], "notes")
        
    def test_update_informant(self):
        response = self.client.put("/api/informants/1/", data = {
            "patAutoID" : 2,
            "fname" : "fname Updated",
            "lname" : "lname Updated",
            "middle_name" : "middle_name Updated",
            "informant_primary" : "informant_primary Updated",
            "informant_relationship" : "informant_relationship Updated",
            "notes" : "notes Updated"
        }) 
        self.assertEqual(response.json["informantID"], 1)
        self.assertEqual(response.json["patAutoID"], 2)
        self.assertEqual(response.json["fname"], "fname Updated")
        self.assertEqual(response.json["lname"], "lname Updated")
        self.assertEqual(response.json["middle_name"], "middle_name Updated")
        self.assertEqual(response.json["informant_primary"], "informant_primary Updated")
        self.assertEqual(response.json["informant_relationship"], "informant_relationship Updated")
        self.assertEqual(response.json["notes"], "notes Updated")
        
    def test_delete_informant(self):
        response = self.client.delete("/api/informants/1/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "InformantID 1 deleted")          
        
class TestInformantAddress(PopulatedDB):
    def test_get_informant_addresses(self):
        response = self.client.get("/api/informantaddresses/")
        self.assertEqual(response.json["InformantAddresses"][0]["informantAddressID"], 1)
        self.assertEqual(response.json["InformantAddresses"][0]["contactInfoSourceLUTID"], 1)
        self.assertEqual(response.json["InformantAddresses"][0]["informantID"], 1)
        self.assertEqual(response.json["InformantAddresses"][0]["contactInfoStatusID"], 1)
        self.assertEqual(response.json["InformantAddresses"][0]["street"], "street")
        self.assertEqual(response.json["InformantAddresses"][0]["street2"], "street2")
        self.assertEqual(response.json["InformantAddresses"][0]["city"], "city")
        self.assertEqual(response.json["InformantAddresses"][0]["state"], "state")
        self.assertEqual(response.json["InformantAddresses"][0]["zip"], "zip")
        self.assertEqual(response.json["InformantAddresses"][0]["address_status"], 1)
        self.assertEqual(response.json["InformantAddresses"][0]["address_status_date"], "2016-02-02")
        self.assertEqual(response.json["InformantAddresses"][0]["address_status_source"], "s1")
        
    def test_get_informant_address(self):
        response = self.client.get("/api/informantaddresses/1/")
        self.assertEqual(response.json["informantAddressID"], 1)
        self.assertEqual(response.json["contactInfoSourceLUTID"], 1)
        self.assertEqual(response.json["informantID"], 1)
        self.assertEqual(response.json["contactInfoStatusID"], 1)
        self.assertEqual(response.json["street"], "street")
        self.assertEqual(response.json["street2"], "street2")
        self.assertEqual(response.json["city"], "city")
        self.assertEqual(response.json["state"], "state")
        self.assertEqual(response.json["zip"], "zip")
        self.assertEqual(response.json["address_status"], 1)
        self.assertEqual(response.json["address_status_date"], "2016-02-02")
        self.assertEqual(response.json["address_status_source"], "s1")
        
    def test_update_informant_address(self):
        response = self.client.put("/api/informantaddresses/1/", data = {
            "contactInfoSourceLUTID" : 2,
            "informantID" : 2,
            "contactInfoStatusID" : 2,
            "street" : "street Updated",
            "street2" : "street2 Updated",
            "city" : "city Updated",
            "state" : "state Updated",
            "zip" : "zip Updated",
            "address_status" : 2,
            "address_status_date" : "2016-02-03",
            "address_status_source" : "s2"
        })
        self.assertEqual(response.json["informantAddressID"], 1)
        self.assertEqual(response.json["contactInfoSourceLUTID"], 2)
        self.assertEqual(response.json["informantID"], 2)
        self.assertEqual(response.json["contactInfoStatusID"], 2)
        self.assertEqual(response.json["street"], "street Updated")
        self.assertEqual(response.json["street2"], "street2 Updated")
        self.assertEqual(response.json["city"], "city Updated")
        self.assertEqual(response.json["state"], "state Updated")
        self.assertEqual(response.json["zip"], "zip Updated")
        self.assertEqual(response.json["address_status"], 2)
        self.assertEqual(response.json["address_status_date"], "2016-02-03")
        self.assertEqual(response.json["address_status_source"], "s2")
        
    def test_delete_informant_address(self):
        response = self.client.delete("/api/informantaddresses/1/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "InformantAddressID 1 deleted")          
        
class TestInformantPhone(PopulatedDB):
    def test_get_informant_phones(self):
        response = self.client.get("/api/informantphones/")
        self.assertEqual(response.json["InformantPhones"][0]["informantPhoneID"], 1)
        self.assertEqual(response.json["InformantPhones"][0]["contactInfoSourceLUTID"], 1)
        self.assertEqual(response.json["InformantPhones"][0]["informantID"], 1)
        self.assertEqual(response.json["InformantPhones"][0]["contactInfoStatusID"], 1)
        self.assertEqual(response.json["InformantPhones"][0]["phone"], "phone")
        self.assertEqual(response.json["InformantPhones"][0]["phone_status"], 1)
        self.assertEqual(response.json["InformantPhones"][0]["phone_source"], "s1")
        self.assertEqual(response.json["InformantPhones"][0]["phone_status_date"], "2016-02-02")
        
    def test_get_informant_phone(self):
        response = self.client.get("/api/informantphones/1/")
        self.assertEqual(response.json["informantPhoneID"], 1)
        self.assertEqual(response.json["contactInfoSourceLUTID"], 1)
        self.assertEqual(response.json["informantID"], 1)
        self.assertEqual(response.json["contactInfoStatusID"], 1)
        self.assertEqual(response.json["phone"], "phone")
        self.assertEqual(response.json["phone_status"], 1)
        self.assertEqual(response.json["phone_source"], "s1")
        self.assertEqual(response.json["phone_status_date"], "2016-02-02")
        
    def test_update_informant_phone(self):
        response = self.client.put("/api/informantphones/1/", data = {
            "contactInfoSourceLUTID" : 2,
            "informantID" : 2,
            "contactInfoStatusID" : 2,
            "phone" : "phone Updated",
            "phone_status" : 2,
            "phone_source" : "s2",
            "phone_status_date" : "2016-02-03"
        })
        self.assertEqual(response.json["informantPhoneID"], 1)
        self.assertEqual(response.json["contactInfoSourceLUTID"], 2)
        self.assertEqual(response.json["informantID"], 2)
        self.assertEqual(response.json["contactInfoStatusID"], 2)
        self.assertEqual(response.json["phone"], "phone Updated")
        self.assertEqual(response.json["phone_status"], 2)
        self.assertEqual(response.json["phone_source"], "s2")
        self.assertEqual(response.json["phone_status_date"], "2016-02-03")
        
    def test_delete_informant_phone(self):
        response = self.client.delete("/api/informantphones/1/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "InformantPhoneID 1 deleted")  
        
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

class TestLog(PopulatedDB):
    def test_get_logs(self):
        response = self.client.get("/api/logs/")
        self.assertEqual(response.json["Logs"][0]["logSubjectLUTID"],1)
        self.assertEqual(response.json["Logs"][0]["projectID"],1)
        self.assertEqual(response.json["Logs"][0]["staffID"],1)
        self.assertEqual(response.json["Logs"][0]["phaseStatusID"],1)
        self.assertEqual(response.json["Logs"][0]["note"],"note")
        self.assertEqual(response.json["Logs"][0]["date"],"2016-02-02")
        
    def test_get_log(self):
        response = self.client.get("/api/logs/1/")
        self.assertEqual(response.json["logSubjectLUTID"],1)
        self.assertEqual(response.json["projectID"],1)
        self.assertEqual(response.json["staffID"],1)
        self.assertEqual(response.json["phaseStatusID"],1)
        self.assertEqual(response.json["note"],"note")
        self.assertEqual(response.json["date"],"2016-02-02")
        
    def test_update_log(self):
        response = self.client.put("/api/logs/1/", data = {
            "logSubjectLUTID" : 2,
            "projectID" : 2,
            "staffID" : 2,
            "phaseStatusID" : 2,
            "note" : "note Updated",
            "date" : "2016-02-03",
        })
        self.assertEqual(response.json["logSubjectLUTID"],2)
        self.assertEqual(response.json["projectID"],2)
        self.assertEqual(response.json["staffID"],2)
        self.assertEqual(response.json["phaseStatusID"],2)
        self.assertEqual(response.json["note"],"note Updated")
        self.assertEqual(response.json["date"],"2016-02-03")
        
    def test_delete_log(self):
        response = self.client.delete("/api/logs/1/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "LogID 1 deleted")  
        
class TestLogSubject(PopulatedDB):
    def test_get_log_subjects(self):
        response = self.client.get("/api/logsubjects/")
        self.assertEqual(response.json["LogSubjects"][0]["log_subject"], "subject")
        
    def test_get_log_subject(self):
        response = self.client.get("/api/logsubjects/1/")
        self.assertEqual(response.json["log_subject"], "subject")
        
    def test_update_log_subject(self):
        response = self.client.put("/api/logsubjects/1/", data = {
            "log_subject" : "subject Updated",
        })
        self.assertEqual(response.json["log_subject"], "subject Updated")
        
    def test_delete_log_subject(self):
        response = self.client.delete("/api/logsubjects/1/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "LogSubjectLUTID 1 deleted")       
               
class TestPatient(PopulatedDB):
    def test_get_patients(self):
        response = self.client.get("/api/patients/")
        self.assertEqual(response.json["Patients"][0]["patID"], "1")
        self.assertEqual(response.json["Patients"][0]["recordID"], 1)
        self.assertEqual(response.json["Patients"][0]["ucrDistID"], 1)
        self.assertEqual(response.json["Patients"][0]["UPDBID"], 1)
        self.assertEqual(response.json["Patients"][0]["fname"], "fname")
        self.assertEqual(response.json["Patients"][0]["lname"], "lname")
        self.assertEqual(response.json["Patients"][0]["maiden_name"], "maiden_name")
        self.assertEqual(response.json["Patients"][0]["alias_fname"], "alias_fname")
        self.assertEqual(response.json["Patients"][0]["alias_lname"], "alias_lname")
        self.assertEqual(response.json["Patients"][0]["alias_middle_name"], "alias_middle")
        self.assertEqual(response.json["Patients"][0]["dob"], "2016-02-02")
        self.assertEqual(response.json["Patients"][0]["SSN"], 999999999)
        self.assertEqual(response.json["Patients"][0]["sex"], "male")
        self.assertEqual(response.json["Patients"][0]["race"], "white")
        self.assertEqual(response.json["Patients"][0]["ethnicity"], "hispanic")
        self.assertEqual(response.json["Patients"][0]["vital_status"], "v1")
        
    def test_get_patient(self):
        response = self.client.get("/api/patients/1/")
        self.assertEqual(response.json["patID"], "1")
        self.assertEqual(response.json["recordID"], 1)
        self.assertEqual(response.json["ucrDistID"], 1)
        self.assertEqual(response.json["UPDBID"], 1)
        self.assertEqual(response.json["fname"], "fname")
        self.assertEqual(response.json["lname"], "lname")
        self.assertEqual(response.json["maiden_name"], "maiden_name")
        self.assertEqual(response.json["alias_fname"], "alias_fname")
        self.assertEqual(response.json["alias_lname"], "alias_lname")
        self.assertEqual(response.json["alias_middle_name"], "alias_middle")
        self.assertEqual(response.json["dob"], "2016-02-02")
        self.assertEqual(response.json["SSN"], 999999999)
        self.assertEqual(response.json["sex"], "male")
        self.assertEqual(response.json["race"], "white")
        self.assertEqual(response.json["ethnicity"], "hispanic")
        self.assertEqual(response.json["vital_status"], "v1")
        
    def test_update_patient(self):
        response = self.client.put("/api/patients/1/", data = {
            "patID" : "2",
            "recordID" : 2,
            "ucrDistID" : 2,
            "UPDBID" : 2,
            "fname" : "fname Updated",
            "lname" : "lname Updated",
            "middle_name" : "mname Updated",
            "maiden_name" : "maiden_name Updated",
            "alias_fname" : "alias_fname Updated",
            "alias_lname" : "alias_lname Updated",
            "alias_middle_name" : "alias_middle Updated",
            "dob" : "2016-02-03",
            "SSN" : "999999990",
            "sex" : "female",
            "race" : "black",
            "ethnicity" : "non-hispanic",
            "vital_status" : "v2"
        })
        self.assertEqual(response.json["patID"], "2")
        self.assertEqual(response.json["recordID"], 2)
        self.assertEqual(response.json["ucrDistID"], 2)
        self.assertEqual(response.json["UPDBID"], 2)
        self.assertEqual(response.json["fname"], "fname Updated")
        self.assertEqual(response.json["lname"], "lname Updated")
        self.assertEqual(response.json["maiden_name"], "maiden_name Updated")
        self.assertEqual(response.json["alias_fname"], "alias_fname Updated")
        self.assertEqual(response.json["alias_lname"], "alias_lname Updated")
        self.assertEqual(response.json["alias_middle_name"], "alias_middle Updated")
        self.assertEqual(response.json["dob"], "2016-02-03")
        self.assertEqual(response.json["SSN"], 999999990)
        self.assertEqual(response.json["sex"], "female")
        self.assertEqual(response.json["race"], "black")
        self.assertEqual(response.json["ethnicity"], "non-hispanic")
        self.assertEqual(response.json["vital_status"], "v2")
        
    def test_delete_patient(self):
        response = self.client.delete("/api/patients/1/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "PatAutoID 1 deleted")      

class TestPatientAddress(PopulatedDB):
    def test_get_patient_addresses(self):
        response = self.client.get("/api/patientaddresses/")
        self.assertEqual(response.json["PatientAddresses"][0]["patAddressID"], 1)
        self.assertEqual(response.json["PatientAddresses"][0]["contactInfoSourceLUTID"], 1)
        self.assertEqual(response.json["PatientAddresses"][0]["patientID"], 1)
        self.assertEqual(response.json["PatientAddresses"][0]["contactInfoStatusLUTID"], 1)
        self.assertEqual(response.json["PatientAddresses"][0]["street"], "street")
        self.assertEqual(response.json["PatientAddresses"][0]["street2"], "street2")
        self.assertEqual(response.json["PatientAddresses"][0]["city"], "city")
        self.assertEqual(response.json["PatientAddresses"][0]["state"], "state")
        self.assertEqual(response.json["PatientAddresses"][0]["zip"], "zip")
        self.assertEqual(response.json["PatientAddresses"][0]["address_status"], 1)
        self.assertEqual(response.json["PatientAddresses"][0]["address_status_date"], "2016-02-02")
        self.assertEqual(response.json["PatientAddresses"][0]["address_status_source"], "s1")
        
    def test_get_patient_address(self):
        response = self.client.get("/api/patientaddresses/1/")
        self.assertEqual(response.json["patAddressID"], 1)
        self.assertEqual(response.json["contactInfoSourceLUTID"], 1)
        self.assertEqual(response.json["patientID"], 1)
        self.assertEqual(response.json["contactInfoStatusLUTID"], 1)
        self.assertEqual(response.json["street"], "street")
        self.assertEqual(response.json["street2"], "street2")
        self.assertEqual(response.json["city"], "city")
        self.assertEqual(response.json["state"], "state")
        self.assertEqual(response.json["zip"], "zip")
        self.assertEqual(response.json["address_status"], 1)
        self.assertEqual(response.json["address_status_date"], "2016-02-02")
        self.assertEqual(response.json["address_status_source"], "s1")
        
    def test_update_patient_address(self):
        response = self.client.put("/api/patientaddresses/1/", data = {
            "contactInfoSourceLUTID" : 2,
            "patientID" : 2,
            "contactInfoStatusLUTID" : 2,
            "street" : "street Updated",
            "street2" : "street2 Updated",
            "city" : "city Updated",
            "state" : "state Updated",
            "zip" : "zip Updated",
            "address_status" : 2,
            "address_status_date" : "2016-02-03",
            "address_status_source" : "s2"
        })
        self.assertEqual(response.json["patAddressID"], 1)
        self.assertEqual(response.json["contactInfoSourceLUTID"], 2)
        self.assertEqual(response.json["patientID"], 2)
        self.assertEqual(response.json["contactInfoStatusLUTID"], 2)
        self.assertEqual(response.json["street"], "street Updated")
        self.assertEqual(response.json["street2"], "street2 Updated")
        self.assertEqual(response.json["city"], "city Updated")
        self.assertEqual(response.json["state"], "state Updated")
        self.assertEqual(response.json["zip"], "zip Updated")
        self.assertEqual(response.json["address_status"], 2)
        self.assertEqual(response.json["address_status_date"], "2016-02-03")
        self.assertEqual(response.json["address_status_source"], "s2")
        
    def test_delete_patient_address(self):
        response = self.client.delete("/api/patientaddresses/1/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "PatAddressID 1 deleted")       

class TestPatientEmail(PopulatedDB):
    def test_get_patient_emails(self):
        response = self.client.get("/api/patientemails/")
        self.assertEqual(response.json["PatientEmails"][0]["emailID"], 1)
        self.assertEqual(response.json["PatientEmails"][0]["contactInfoSourceLUTID"], 1)
        self.assertEqual(response.json["PatientEmails"][0]["patientID"], 1)
        self.assertEqual(response.json["PatientEmails"][0]["contactInfoStatusID"], 1)
        self.assertEqual(response.json["PatientEmails"][0]["email"], "email")
        self.assertEqual(response.json["PatientEmails"][0]["email_status"], 1)
        self.assertEqual(response.json["PatientEmails"][0]["email_source"], 1)
        self.assertEqual(response.json["PatientEmails"][0]["email_status_date"], "2016-02-02")
        
    def test_get_patient_email(self):
        response = self.client.get("/api/patientemails/1/")
        self.assertEqual(response.json["emailID"], 1)
        self.assertEqual(response.json["contactInfoSourceLUTID"], 1)
        self.assertEqual(response.json["patientID"], 1)
        self.assertEqual(response.json["contactInfoStatusID"], 1)
        self.assertEqual(response.json["email"], "email")
        self.assertEqual(response.json["email_status"], 1)
        self.assertEqual(response.json["email_source"], 1)
        self.assertEqual(response.json["email_status_date"], "2016-02-02")
        
    def test_update_patient_email(self):
        response = self.client.put("/api/patientemails/1/", data = {
            "contactInfoSourceLUTID" : 2,
            "patientID" : 2,
            "contactInfoStatusID" : 2,
            "email" : "email Updated",
            "email_status" : 2,
            "email_source" : 2,
            "email_status_date" : "2016-02-03"
        })
        self.assertEqual(response.json["emailID"], 1)
        self.assertEqual(response.json["contactInfoSourceLUTID"], 2)
        self.assertEqual(response.json["patientID"], 2)
        self.assertEqual(response.json["contactInfoStatusID"], 2)
        self.assertEqual(response.json["email"], "email Updated")
        self.assertEqual(response.json["email_status"], 2)
        self.assertEqual(response.json["email_source"], 2)
        self.assertEqual(response.json["email_status_date"], "2016-02-03")
        
    def test_delete_patient_email(self):
        response = self.client.delete("/api/patientemails/1/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "EmailID 1 deleted")           

class TestPatientPhone(PopulatedDB):
    def test_get_patient_phone(self):
        response = self.client.get("/api/patientphones/")
        self.assertEqual(response.json["PatientPhones"][0]["patPhoneID"], 1)
        self.assertEqual(response.json["PatientPhones"][0]["contactInfoSourceLUTID"], 1)
        self.assertEqual(response.json["PatientPhones"][0]["patientID"], 1)
        self.assertEqual(response.json["PatientPhones"][0]["contactInfoStatusID"], 1)
        self.assertEqual(response.json["PatientPhones"][0]["phone"], "phone")
        self.assertEqual(response.json["PatientPhones"][0]["phone_status"], 1)
        self.assertEqual(response.json["PatientPhones"][0]["phone_source"], "s1")
        self.assertEqual(response.json["PatientPhones"][0]["phone_status_date"], "2016-02-02")
        
    def test_get_patient_phone(self):
        response = self.client.get("/api/patientphones/1/")
        self.assertEqual(response.json["patPhoneID"], 1)
        self.assertEqual(response.json["contactInfoSourceLUTID"], 1)
        self.assertEqual(response.json["patientID"], 1)
        self.assertEqual(response.json["contactInfoStatusID"], 1)
        self.assertEqual(response.json["phone"], "phone")
        self.assertEqual(response.json["phone_status"], 1)
        self.assertEqual(response.json["phone_source"], "s1")
        self.assertEqual(response.json["phone_status_date"], "2016-02-02")
        
    def test_update_patient_phone(self):
        response = self.client.put("/api/patientphones/1/", data = {
            "contactInfoSourceLUTID" : 2,
            "patientID" : 2,
            "contactInfoStatusID" : 2,
            "phone" : "phone Updated",
            "phone_status" : 2,
            "phone_source" : "s2",
            "phone_status_date" : "2016-02-03"
        })
        self.assertEqual(response.json["patPhoneID"], 1)
        self.assertEqual(response.json["contactInfoSourceLUTID"], 2)
        self.assertEqual(response.json["patientID"], 2)
        self.assertEqual(response.json["contactInfoStatusID"], 2)
        self.assertEqual(response.json["phone"], "phone Updated")
        self.assertEqual(response.json["phone_status"], 2)
        self.assertEqual(response.json["phone_source"], "s2")
        self.assertEqual(response.json["phone_status_date"], "2016-02-03")
        
    def test_delete_patient_phone(self):
        response = self.client.delete("/api/patientphones/1/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "PatPhoneID 1 deleted")      

class TestPatientProjectStatus(PopulatedDB):
    def test_get_patient_project_statuses(self):
        response = self.client.get("/api/patientprojectstatuses/")
        self.assertEqual(response.json["PatientProjectStatuses"][0]["patientProjectStatusID"], 1)
        self.assertEqual(response.json["PatientProjectStatuses"][0]["patientProjectStatusLUTID"], 1)
        self.assertEqual(response.json["PatientProjectStatuses"][0]["projectPatientID"], 1)
        
    def test_get_patient_project_status(self):
        response = self.client.get("/api/patientprojectstatuses/1/")
        self.assertEqual(response.json["patientProjectStatusID"], 1)
        self.assertEqual(response.json["patientProjectStatusLUTID"], 1)
        self.assertEqual(response.json["projectPatientID"], 1)
        
    def test_update_patient_project_status(self):
        response = self.client.put("/api/patientprojectstatuses/1/", data = {
            "patientProjectStatusLUTID" : 2,
            "projectPatientID" : 2
        })
        self.assertEqual(response.json["patientProjectStatusID"], 1)
        self.assertEqual(response.json["patientProjectStatusLUTID"], 2)
        self.assertEqual(response.json["projectPatientID"], 2)
        
    def test_delete_patient_project_status(self):
        response = self.client.delete("/api/patientprojectstatuses/1/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "PatientProjectStatusID 1 deleted")   

class TestPatientProjectStatusLUT(PopulatedDB):
    def test_get_patient_project_status_types(self):
        response = self.client.get("/api/patientprojectstatustypes/")
        self.assertEqual(response.json["PatientProjectStatusTypes"][0]["patientProjectStatusTypeID"], 1)
        self.assertEqual(response.json["PatientProjectStatusTypes"][0]["status_description"], "desc")

    def test_get_patient_project_status_type(self):
        response = self.client.get("/api/patientprojectstatustypes/1/")
        self.assertEqual(response.json["patientProjectStatusTypeID"], 1)
        self.assertEqual(response.json["status_description"], "desc")

    def test_update_patient_project_status_type(self):
        response = self.client.put("/api/patientprojectstatustypes/1/", data = {
            "status_description" : "desc Updated"
        })
        self.assertEqual(response.json["patientProjectStatusTypeID"], 1)
        self.assertEqual(response.json["status_description"], "desc Updated")

    def test_delete_patient_project_status_type(self):
        response = self.client.delete("/api/patientprojectstatustypes/1/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "PatientProjectStatusTypeID 1 deleted")             
        
class TestPhaseStatus(PopulatedDB):
    def test_get_phase_statuses(self):
        response = self.client.get("/api/phasestatuses/")
        self.assertEqual(response.json["PhaseStatuses"][0]["phase_status"], "status")
        self.assertEqual(response.json["PhaseStatuses"][0]["phase_description"], "desc")
        
    def test_get_phase_status(self):
        response = self.client.get("/api/phasestatuses/1/")
        self.assertEqual(response.json["phase_status"], "status")
        self.assertEqual(response.json["phase_description"], "desc")
        
    def test_update_phase_status(self):
        response = self.client.put("/api/phasestatuses/1/", data = {
            "phase_status" : "status Updated",
            "phase_description": "desc Updated"
        })
        self.assertEqual(response.json["phase_status"], "status Updated")
        self.assertEqual(response.json["phase_description"], "desc Updated")
        
    def test_delete_phase_status(self):
        response = self.client.delete("/api/phasestatuses/1/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "LogPhaseID 1 deleted")       

class TestPhysician(PopulatedDB):
    def test_get_physicians(self):
        response = self.client.get("/api/physicians/")
        self.assertEqual(response.json["Physicians"][0]["fname"], "fname")
        self.assertEqual(response.json["Physicians"][0]["lname"], "lname")
        self.assertEqual(response.json["Physicians"][0]["middle_name"], "middle_name")
        self.assertEqual(response.json["Physicians"][0]["credentials"], "credentials")
        self.assertEqual(response.json["Physicians"][0]["specialty"], "specialty")
        self.assertEqual(response.json["Physicians"][0]["alias_fname"], "alias_fname")
        self.assertEqual(response.json["Physicians"][0]["alias_lname"], "alias_lname")
        self.assertEqual(response.json["Physicians"][0]["alias_middle_name"], "alias_middle_name")
        self.assertEqual(response.json["Physicians"][0]["physician_status"], 1)
        self.assertEqual(response.json["Physicians"][0]["physician_status_date"], "2016-02-02")
        self.assertEqual(response.json["Physicians"][0]["email"], "email")
        
    def test_get_physician(self):
        response = self.client.get("/api/physicians/1/")
        self.assertEqual(response.json["fname"], "fname")
        self.assertEqual(response.json["lname"], "lname")
        self.assertEqual(response.json["middle_name"], "middle_name")
        self.assertEqual(response.json["credentials"], "credentials")
        self.assertEqual(response.json["specialty"], "specialty")
        self.assertEqual(response.json["alias_fname"], "alias_fname")
        self.assertEqual(response.json["alias_lname"], "alias_lname")
        self.assertEqual(response.json["alias_middle_name"], "alias_middle_name")
        self.assertEqual(response.json["physician_status"], 1)
        self.assertEqual(response.json["physician_status_date"], "2016-02-02")
        self.assertEqual(response.json["email"], "email")
        
    def test_update_physician(self):
        response = self.client.put("/api/physicians/1/", data = {
            "fname" : "fname2",
            "lname" : "lname2",
            "middle_name" : "middle_name2",
            "credentials" : "credentials2",
            "specialty" : "specialty2",
            "alias_fname" : "alias_fname2",
            "alias_lname" : "alias_lname2",
            "alias_middle_name" : "alias_middle_name2",
            "physician_status" : 2,
            "physician_status_date" : "2016-02-03",
            "email" : "email2"
        })
        self.assertEqual(response.json["fname"], "fname2")
        self.assertEqual(response.json["lname"], "lname2")
        self.assertEqual(response.json["middle_name"], "middle_name2")
        self.assertEqual(response.json["credentials"], "credentials2")
        self.assertEqual(response.json["specialty"], "specialty2")
        self.assertEqual(response.json["alias_fname"], "alias_fname2")
        self.assertEqual(response.json["alias_lname"], "alias_lname2")
        self.assertEqual(response.json["alias_middle_name"], "alias_middle_name2")
        self.assertEqual(response.json["physician_status"], 2)
        self.assertEqual(response.json["physician_status_date"], "2016-02-03")
        self.assertEqual(response.json["email"], "email2")
        
    def test_delete_physician(self):
        response = self.client.delete("/api/physicians/1/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "PhysicianID 1 deleted")       

class TestPhysicianAddress(PopulatedDB):
    def test_get_physician_addresses(self):
        response = self.client.get("/api/physicianaddresses/")
        self.assertEqual(response.json["PhysicianAddresses"][0]["physicianAddressID"], 1)
        self.assertEqual(response.json["PhysicianAddresses"][0]["contactInfoSourceLUTID"], 1)
        self.assertEqual(response.json["PhysicianAddresses"][0]["physicianID"], 1)
        self.assertEqual(response.json["PhysicianAddresses"][0]["contactInfoStatusLUTID"], 1)
        self.assertEqual(response.json["PhysicianAddresses"][0]["street"], "street")
        self.assertEqual(response.json["PhysicianAddresses"][0]["street2"], "street2")
        self.assertEqual(response.json["PhysicianAddresses"][0]["city"], "city")
        self.assertEqual(response.json["PhysicianAddresses"][0]["state"], "state")
        self.assertEqual(response.json["PhysicianAddresses"][0]["zip"], "zip")
        self.assertEqual(response.json["PhysicianAddresses"][0]["address_status"], 1)
        self.assertEqual(response.json["PhysicianAddresses"][0]["address_status_date"], "2016-02-02")
        self.assertEqual(response.json["PhysicianAddresses"][0]["address_status_source"], "s1")
        
    def test_get_physician_address(self):
        response = self.client.get("/api/physicianaddresses/1/")
        self.assertEqual(response.json["physicianAddressID"], 1)
        self.assertEqual(response.json["contactInfoSourceLUTID"], 1)
        self.assertEqual(response.json["physicianID"], 1)
        self.assertEqual(response.json["contactInfoStatusLUTID"], 1)
        self.assertEqual(response.json["street"], "street")
        self.assertEqual(response.json["street2"], "street2")
        self.assertEqual(response.json["city"], "city")
        self.assertEqual(response.json["state"], "state")
        self.assertEqual(response.json["zip"], "zip")
        self.assertEqual(response.json["address_status"], 1)
        self.assertEqual(response.json["address_status_date"], "2016-02-02")
        self.assertEqual(response.json["address_status_source"], "s1")
        
    def test_update_physician_address(self):
        response = self.client.put("/api/physicianaddresses/1/", data = {
            "contactInfoSourceLUTID" : 2,
            "physicianID" : 2,
            "contactInfoStatusLUTID" : 2,
            "street" : "street Updated",
            "street2" : "street2 Updated",
            "city" : "city Updated",
            "state" : "state Updated",
            "zip" : "zip Updated",
            "address_status" : 2,
            "address_status_date" : "2016-02-03",
            "address_status_source" : "s2"
        })
        self.assertEqual(response.json["physicianAddressID"], 1)
        self.assertEqual(response.json["contactInfoSourceLUTID"], 2)
        self.assertEqual(response.json["physicianID"], 2)
        self.assertEqual(response.json["contactInfoStatusLUTID"], 2)
        self.assertEqual(response.json["street"], "street Updated")
        self.assertEqual(response.json["street2"], "street2 Updated")
        self.assertEqual(response.json["city"], "city Updated")
        self.assertEqual(response.json["state"], "state Updated")
        self.assertEqual(response.json["zip"], "zip Updated")
        self.assertEqual(response.json["address_status"], 2)
        self.assertEqual(response.json["address_status_date"], "2016-02-03")
        self.assertEqual(response.json["address_status_source"], "s2")
        
    def test_delete_physician_address(self):
        response = self.client.delete("/api/physicianaddresses/1/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "PhysicianAddressID 1 deleted")       

class TestPhysicianFacility(PopulatedDB):
    def test_get_physician_facilities(self):
        response = self.client.get("/api/physicianfacilities/")
        self.assertEqual(response.json["PhysicianFacilities"][0]["physFacilityID"], 1)
        self.assertEqual(response.json["PhysicianFacilities"][0]["physicianID"], 1)
        self.assertEqual(response.json["PhysicianFacilities"][0]["facilityID"], 1)
        self.assertEqual(response.json["PhysicianFacilities"][0]["phys_facility_status"], "s1")
        self.assertEqual(response.json["PhysicianFacilities"][0]["phys_facility_status_date"], "2016-02-02")
        
    def test_get_physician_facility(self):
        response = self.client.get("/api/physicianfacilities/1/")
        self.assertEqual(response.json["physFacilityID"], 1)
        self.assertEqual(response.json["physicianID"], 1)
        self.assertEqual(response.json["facilityID"], 1)
        self.assertEqual(response.json["phys_facility_status"], "s1")
        self.assertEqual(response.json["phys_facility_status_date"], "2016-02-02")
        
    def test_update_physician_facility(self):
        response = self.client.put("/api/physicianfacilities/1/", data = {
            "facilityID" : 2,
            "physicianID" : 2,
            "phys_facility_status" : "s2",
            "phys_facility_status_date" : "2016-02-03"
        })
        self.assertEqual(response.json["physFacilityID"], 1)
        self.assertEqual(response.json["physicianID"], 2)
        self.assertEqual(response.json["facilityID"], 2)
        self.assertEqual(response.json["phys_facility_status"], "s2")
        self.assertEqual(response.json["phys_facility_status_date"], "2016-02-03")
        
    def test_delete_physician_facility(self):
        response = self.client.delete("/api/physicianfacilities/1/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "PhysFacilityID 1 deleted")      
        
class TestPhysicianPhone(PopulatedDB):
    def test_get_physician_phone(self):
        response = self.client.get("/api/physicianphones/")
        self.assertEqual(response.json["PhysicianPhones"][0]["physicianPhoneID"], 1)
        self.assertEqual(response.json["PhysicianPhones"][0]["contactInfoSourceLUTID"], 1)
        self.assertEqual(response.json["PhysicianPhones"][0]["physicianID"], 1)
        self.assertEqual(response.json["PhysicianPhones"][0]["contactInfoStatusID"], 1)
        self.assertEqual(response.json["PhysicianPhones"][0]["phone"], "phone")
        self.assertEqual(response.json["PhysicianPhones"][0]["phone_type"], "phone_type")
        self.assertEqual(response.json["PhysicianPhones"][0]["phone_status"], 1)
        self.assertEqual(response.json["PhysicianPhones"][0]["phone_source"], "s1")
        self.assertEqual(response.json["PhysicianPhones"][0]["phone_status_date"], "2016-02-02")
        
    def test_get_physician_phone(self):
        response = self.client.get("/api/physicianphones/1/")
        self.assertEqual(response.json["physicianPhoneID"], 1)
        self.assertEqual(response.json["contactInfoSourceLUTID"], 1)
        self.assertEqual(response.json["physicianID"], 1)
        self.assertEqual(response.json["contactInfoStatusID"], 1)
        self.assertEqual(response.json["phone"], "phone")
        self.assertEqual(response.json["phone_type"], "phone_type")
        self.assertEqual(response.json["phone_status"], 1)
        self.assertEqual(response.json["phone_source"], "s1")
        self.assertEqual(response.json["phone_status_date"], "2016-02-02")
        
    def test_update_physician_phone(self):
        response = self.client.put("/api/physicianphones/1/", data = {
            "contactInfoSourceLUTID" : 2,
            "physicianID" : 2,
            "contactInfoStatusID" : 2,
            "phone" : "phone Updated",
            "phone_type": "phone_type Updated",
            "phone_status" : 2,
            "phone_source" : "s2",
            "phone_status_date" : "2016-02-03"
        })
        self.assertEqual(response.json["physicianPhoneID"], 1)
        self.assertEqual(response.json["contactInfoSourceLUTID"], 2)
        self.assertEqual(response.json["physicianID"], 2)
        self.assertEqual(response.json["contactInfoStatusID"], 2)
        self.assertEqual(response.json["phone"], "phone Updated")
        self.assertEqual(response.json["phone_type"], "phone_type Updated")
        self.assertEqual(response.json["phone_status"], 2)
        self.assertEqual(response.json["phone_source"], "s2")
        self.assertEqual(response.json["phone_status_date"], "2016-02-03")
        
    def test_delete_physician_phone(self):
        response = self.client.delete("/api/physicianphones/1/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "PhysicianPhoneID 1 deleted")      
        
class TestPhysicianToCTC(PopulatedDB):
    def test_get_physician_to_ctcs(self):
        response = self.client.get("/api/physiciantoctcs/")
        self.assertEqual(response.json["PhysicianToCTCs"][0]["physicianID"], 1)
        self.assertEqual(response.json["PhysicianToCTCs"][0]["ctcID"], 1)
        
    def test_get_physician_to_ctc(self):
        response = self.client.get("/api/physiciantoctcs/1/")
        self.assertEqual(response.json["physicianID"], 1)
        self.assertEqual(response.json["ctcID"], 1)
        
    def test_update_physician_to_ctc(self):
        response = self.client.put("/api/physiciantoctcs/1/", data = {
            "physicianID" : 2,
            "ctcID": 2
        })
        self.assertEqual(response.json["physicianID"], 2)
        self.assertEqual(response.json["ctcID"], 2)
        
    def test_delete_physician_to_ctc(self):
        response = self.client.delete("/api/physiciantoctcs/1/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "PhysicianCTCID 1 deleted")       

class TestPreApplication(PopulatedDB):
    def test_get_pre_applications(self):
        response = self.client.get("/api/preapplications/")
        self.assertEqual(response.json["PreApplications"][0]["projectID"], 1)
        self.assertEqual(response.json["PreApplications"][0]["pi_fname"], "pi_fname")
        self.assertEqual(response.json["PreApplications"][0]["pi_lname"], "pi_lname")
        self.assertEqual(response.json["PreApplications"][0]["pi_phone"], "pi_phone")
        self.assertEqual(response.json["PreApplications"][0]["pi_email"], "pi_email")
        self.assertEqual(response.json["PreApplications"][0]["contact_fname"], "contact_fname")
        self.assertEqual(response.json["PreApplications"][0]["contact_lname"], "contact_lname")
        self.assertEqual(response.json["PreApplications"][0]["contact_phone"], "contact_phone")
        self.assertEqual(response.json["PreApplications"][0]["contact_email"], "contact_email")
        self.assertEqual(response.json["PreApplications"][0]["institution"], "institution")
        self.assertEqual(response.json["PreApplications"][0]["institution2"], "institution2")        
        self.assertEqual(response.json["PreApplications"][0]["uid"], "uid")
        self.assertEqual(response.json["PreApplications"][0]["udoh"], 1)
        self.assertEqual(response.json["PreApplications"][0]["project_title"], "project_title")
        self.assertEqual(response.json["PreApplications"][0]["purpose"], "purpose")
        self.assertEqual(response.json["PreApplications"][0]["irb0"], True)
        self.assertEqual(response.json["PreApplications"][0]["irb1"], True)
        self.assertEqual(response.json["PreApplications"][0]["irb2"], True)
        self.assertEqual(response.json["PreApplications"][0]["irb3"], True)
        self.assertEqual(response.json["PreApplications"][0]["irb4"], True)
        self.assertEqual(response.json["PreApplications"][0]["other_irb"], "other_irb") 
        self.assertEqual(response.json["PreApplications"][0]["updb"], True)
        self.assertEqual(response.json["PreApplications"][0]["pt_contact"], True)
        self.assertEqual(response.json["PreApplications"][0]["start_date"], "2016-02-02")
        self.assertEqual(response.json["PreApplications"][0]["link"], True)
        self.assertEqual(response.json["PreApplications"][0]["delivery_date"], "2016-02-02")
        self.assertEqual(response.json["PreApplications"][0]["description"], "description")
        
    def test_get_pre_application(self):
        response = self.client.get("/api/preapplications/1/")
        self.assertEqual(response.json["projectID"], 1)
        self.assertEqual(response.json["pi_fname"], "pi_fname")
        self.assertEqual(response.json["pi_lname"], "pi_lname")
        self.assertEqual(response.json["pi_phone"], "pi_phone")
        self.assertEqual(response.json["pi_email"], "pi_email")
        self.assertEqual(response.json["contact_fname"], "contact_fname")
        self.assertEqual(response.json["contact_lname"], "contact_lname")
        self.assertEqual(response.json["contact_phone"], "contact_phone")
        self.assertEqual(response.json["contact_email"], "contact_email")
        self.assertEqual(response.json["institution"], "institution")
        self.assertEqual(response.json["institution2"], "institution2")        
        self.assertEqual(response.json["uid"], "uid")
        self.assertEqual(response.json["udoh"], 1)
        self.assertEqual(response.json["project_title"], "project_title")
        self.assertEqual(response.json["purpose"], "purpose")
        self.assertEqual(response.json["irb0"], True)
        self.assertEqual(response.json["irb1"], True)
        self.assertEqual(response.json["irb2"], True)
        self.assertEqual(response.json["irb3"], True)
        self.assertEqual(response.json["irb4"], True)
        self.assertEqual(response.json["other_irb"], "other_irb") 
        self.assertEqual(response.json["updb"], True)
        self.assertEqual(response.json["pt_contact"], True)
        self.assertEqual(response.json["start_date"], "2016-02-02")
        self.assertEqual(response.json["link"], True)
        self.assertEqual(response.json["delivery_date"], "2016-02-02")
        self.assertEqual(response.json["description"], "description")
        
    def test_update_pre_application(self):
        response = self.client.put("/api/preapplications/1/", data = {
            "projectID" : 2,
            "pi_fname" : "pi_fname2",
            "pi_lname" : "pi_lname2",
            "pi_email" : "pi_email2",
            "pi_phone" : "pi_phone2",
            "contact_fname" : "contact_fname2",
            "contact_lname" : "contact_lname2",
            "contact_phone" : "contact_phone2",
            "contact_email" : "contact_email2",
            "institution" : "institution2",
            "institution2" : "institution22",
            "uid" : "uid2",
            "udoh" : 2,
            "project_title" : "project_title2",
            "purpose" : "purpose2",
            "irb0" : False,
            "irb1" : False,
            "irb2" : False,
            "irb3" : False,
            "irb4" : False,
            "other_irb" : "other_irb2",
            "updb" : False,
            "pt_contact" : False,
            "start_date" : "2016-02-03",
            "link" : False,
            "delivery_date" : "2016-02-03",
            "description" : "description2"
        })
        self.assertEqual(response.json["projectID"], 2)
        self.assertEqual(response.json["pi_fname"], "pi_fname2")
        self.assertEqual(response.json["pi_lname"], "pi_lname2")
        self.assertEqual(response.json["pi_phone"], "pi_phone2")
        self.assertEqual(response.json["pi_email"], "pi_email2")
        self.assertEqual(response.json["contact_fname"], "contact_fname2")
        self.assertEqual(response.json["contact_lname"], "contact_lname2")
        self.assertEqual(response.json["contact_phone"], "contact_phone2")
        self.assertEqual(response.json["contact_email"], "contact_email2")
        self.assertEqual(response.json["institution"], "institution2")
        self.assertEqual(response.json["institution2"], "institution22")        
        self.assertEqual(response.json["uid"], "uid2")
        self.assertEqual(response.json["udoh"], 2)
        self.assertEqual(response.json["project_title"], "project_title2")
        self.assertEqual(response.json["purpose"], "purpose2")
        self.assertEqual(response.json["irb0"], False)
        self.assertEqual(response.json["irb1"], False)
        self.assertEqual(response.json["irb2"], False)
        self.assertEqual(response.json["irb3"], False)
        self.assertEqual(response.json["irb4"], False)
        self.assertEqual(response.json["other_irb"], "other_irb2") 
        self.assertEqual(response.json["updb"], False)
        self.assertEqual(response.json["pt_contact"], False)
        self.assertEqual(response.json["start_date"], "2016-02-03")
        self.assertEqual(response.json["link"], False)
        self.assertEqual(response.json["delivery_date"], "2016-02-03")
        self.assertEqual(response.json["description"], "description2")
        
    def test_delete_pre_application(self):
        response = self.client.delete("/api/preapplications/1/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "PreApplicationID 1 deleted")    
        
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

class TestProjectPatient(PopulatedDB):
    def test_get_project_statuses(self):
        response = self.client.get("/api/projectpatients/")
        self.assertEqual(response.json["ProjectPatients"][0]["participantID"], 1)
        self.assertEqual(response.json["ProjectPatients"][0]["projectID"], 1)
        self.assertEqual(response.json["ProjectPatients"][0]["staffID"], 1)
        self.assertEqual(response.json["ProjectPatients"][0]["ctcID"], 1)
        self.assertEqual(response.json["ProjectPatients"][0]["current_age"], 1)
        self.assertEqual(response.json["ProjectPatients"][0]["batch"], 1)
        self.assertEqual(response.json["ProjectPatients"][0]["sitegrp"], 1)
        self.assertEqual(response.json["ProjectPatients"][0]["final_code"], 1)
        self.assertEqual(response.json["ProjectPatients"][0]["final_code_date"], "2016-02-02")
        self.assertEqual(response.json["ProjectPatients"][0]["enrollment_date"], "2016-02-02")
        self.assertEqual(response.json["ProjectPatients"][0]["date_coord_signed"], "2016-02-02")
        self.assertEqual(response.json["ProjectPatients"][0]["import_date"], "2016-02-02")
        self.assertEqual(response.json["ProjectPatients"][0]["final_code_staff"], 1)
        self.assertEqual(response.json["ProjectPatients"][0]["enrollment_staff"], 1)
        self.assertEqual(response.json["ProjectPatients"][0]["date_coord_signed_staff"], "2016-02-02")
        self.assertEqual(response.json["ProjectPatients"][0]["abstract_status"], 1)
        self.assertEqual(response.json["ProjectPatients"][0]["abstract_status_date"], "2016-02-02")
        self.assertEqual(response.json["ProjectPatients"][0]["abstract_status_staff"], 1)
        self.assertEqual(response.json["ProjectPatients"][0]["sent_to_abstractor"], "2016-02-02")
        self.assertEqual(response.json["ProjectPatients"][0]["sent_to_abstractor_staff"], 1)
        self.assertEqual(response.json["ProjectPatients"][0]["abstracted_date"], "2016-02-02")
        self.assertEqual(response.json["ProjectPatients"][0]["abstractor_initials"], "atp")
        self.assertEqual(response.json["ProjectPatients"][0]["researcher_date"], "2016-02-02")
        self.assertEqual(response.json["ProjectPatients"][0]["researcher_staff"], 1)
        self.assertEqual(response.json["ProjectPatients"][0]["consent_link"], "link")
        self.assertEqual(response.json["ProjectPatients"][0]["tracing_status"], 1)
        self.assertEqual(response.json["ProjectPatients"][0]["med_record_release_signed"], True)
        self.assertEqual(response.json["ProjectPatients"][0]["med_record_release_link"], "link")
        self.assertEqual(response.json["ProjectPatients"][0]["med_record_release_staff"], 1)
        self.assertEqual(response.json["ProjectPatients"][0]["med_record_release_date"], "2016-02-02")
        self.assertEqual(response.json["ProjectPatients"][0]["survey_to_researcher"], "2016-02-02")
        self.assertEqual(response.json["ProjectPatients"][0]["survey_to_researcher_staff"], 1)

        
    def test_get_project_patient(self):
        response = self.client.get("/api/projectpatients/1/")
        self.assertEqual(response.json["participantID"], 1)
        self.assertEqual(response.json["projectID"], 1)
        self.assertEqual(response.json["staffID"], 1)
        self.assertEqual(response.json["ctcID"], 1)
        self.assertEqual(response.json["current_age"], 1)
        self.assertEqual(response.json["batch"], 1)
        self.assertEqual(response.json["sitegrp"], 1)
        self.assertEqual(response.json["final_code"], 1)
        self.assertEqual(response.json["final_code_date"], "2016-02-02")
        self.assertEqual(response.json["enrollment_date"], "2016-02-02")
        self.assertEqual(response.json["date_coord_signed"], "2016-02-02")
        self.assertEqual(response.json["import_date"], "2016-02-02")
        self.assertEqual(response.json["final_code_staff"], 1)
        self.assertEqual(response.json["enrollment_staff"], 1)
        self.assertEqual(response.json["date_coord_signed_staff"], "2016-02-02")
        self.assertEqual(response.json["abstract_status"], 1)
        self.assertEqual(response.json["abstract_status_date"], "2016-02-02")
        self.assertEqual(response.json["abstract_status_staff"], 1)
        self.assertEqual(response.json["sent_to_abstractor"], "2016-02-02")
        self.assertEqual(response.json["sent_to_abstractor_staff"], 1)
        self.assertEqual(response.json["abstracted_date"], "2016-02-02")
        self.assertEqual(response.json["abstractor_initials"], "atp")
        self.assertEqual(response.json["researcher_date"], "2016-02-02")
        self.assertEqual(response.json["researcher_staff"], 1)
        self.assertEqual(response.json["consent_link"], "link")
        self.assertEqual(response.json["tracing_status"], 1)
        self.assertEqual(response.json["med_record_release_signed"], True)
        self.assertEqual(response.json["med_record_release_link"], "link")
        self.assertEqual(response.json["med_record_release_staff"], 1)
        self.assertEqual(response.json["med_record_release_date"], "2016-02-02")
        self.assertEqual(response.json["survey_to_researcher"], "2016-02-02")
        self.assertEqual(response.json["survey_to_researcher_staff"], 1)
        
    def test_update_project_patient(self):
        response = self.client.put("/api/projectpatients/1/", data = {
            "projectID" : 2,
            "staffID" : 2,
            "ctcID" : 2,
            "current_age" : 2,
            "batch"  : 2,
            "sitegrp" : 2,
            "final_code" : 2,
            "final_code_date" : "2016-02-03",
            "enrollment_date" : "2016-02-03",
            "date_coord_signed" : "2016-02-03",
            "import_date" : "2016-02-03",
            "final_code_staff" : 2,
            "enrollment_staff" : 2,
            "date_coord_signed_staff"  : "2016-02-03",
            "abstract_status" : 2,
            "abstract_status_date" : "2016-02-03",
            "abstract_status_staff" : 2,
            "sent_to_abstractor"  : "2016-02-03",
            "sent_to_abstractor_staff" : 2,
            "abstracted_date" : "2016-02-03",
            "abstractor_initials" : "atp Updated",
            "researcher_date" : "2016-02-03",
            "researcher_staff" : 2,
            "consent_link" : "link Updated",
            "tracing_status" : 2,
            "med_record_release_signed" : False,
            "med_record_release_link" : "link Updated",
            "med_record_release_staff" : 2,
            "med_record_release_date"  : "2016-02-03",
            "survey_to_researcher"  : "2016-02-03",
            "survey_to_researcher_staff" : 2
        })
        self.assertEqual(response.json["participantID"], 1)
        self.assertEqual(response.json["projectID"], 2)
        self.assertEqual(response.json["staffID"], 2)
        self.assertEqual(response.json["ctcID"], 2)
        self.assertEqual(response.json["current_age"], 2)
        self.assertEqual(response.json["batch"], 2)
        self.assertEqual(response.json["sitegrp"], 2)
        self.assertEqual(response.json["final_code"], 2)
        self.assertEqual(response.json["final_code_date"], "2016-02-03")
        self.assertEqual(response.json["enrollment_date"], "2016-02-03")
        self.assertEqual(response.json["date_coord_signed"], "2016-02-03")
        self.assertEqual(response.json["import_date"], "2016-02-03")
        self.assertEqual(response.json["final_code_staff"], 2)
        self.assertEqual(response.json["enrollment_staff"], 2)
        self.assertEqual(response.json["date_coord_signed_staff"], "2016-02-03")
        self.assertEqual(response.json["abstract_status"], 2)
        self.assertEqual(response.json["abstract_status_date"], "2016-02-03")
        self.assertEqual(response.json["abstract_status_staff"], 2)
        self.assertEqual(response.json["sent_to_abstractor"], "2016-02-03")
        self.assertEqual(response.json["sent_to_abstractor_staff"], 2)
        self.assertEqual(response.json["abstracted_date"], "2016-02-03")
        self.assertEqual(response.json["abstractor_initials"], "atp Updated")
        self.assertEqual(response.json["researcher_date"], "2016-02-03")
        self.assertEqual(response.json["researcher_staff"], 2)
        self.assertEqual(response.json["consent_link"], "link Updated")
        self.assertEqual(response.json["tracing_status"], 2)
        self.assertEqual(response.json["med_record_release_signed"], False)
        self.assertEqual(response.json["med_record_release_link"], "link Updated")
        self.assertEqual(response.json["med_record_release_staff"], 2)
        self.assertEqual(response.json["med_record_release_date"], "2016-02-03")
        self.assertEqual(response.json["survey_to_researcher"], "2016-02-03")
        self.assertEqual(response.json["survey_to_researcher_staff"], 2)
        
    def test_delete_project_patient(self):
        response = self.client.delete("/api/projectpatients/1/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "ParticipantID 1 deleted")       

class TestProjectStaff(PopulatedDB):
    def test_get_staffs(self):
        response = self.client.get("/api/projectstaff/")
        self.assertEqual(response.json["ProjectStaff"][0]["staffRoleLUTID"], 1)
        self.assertEqual(response.json["ProjectStaff"][0]["projectID"], 1)
        self.assertEqual(response.json["ProjectStaff"][0]["staffID"], 1)
        self.assertEqual(response.json["ProjectStaff"][0]["role"], 1)
        self.assertEqual(response.json["ProjectStaff"][0]["date_pledge"], "2016-02-02")
        self.assertEqual(response.json["ProjectStaff"][0]["date_revoked"], "2016-02-02")
        self.assertEqual(response.json["ProjectStaff"][0]["contact"], "yes")
        self.assertEqual(response.json["ProjectStaff"][0]["inactive"], "no")
        self.assertEqual(response.json["ProjectStaff"][0]["human_sub_training_exp"], "2016-02-02")
        self.assertEqual(response.json["ProjectStaff"][0]["human_sub_type_id"], 1)
        self.assertEqual(response.json["ProjectStaff"][0]["study_role"], 1)

    def test_get_staff(self):
        response = self.client.get("/api/projectstaff/1/")
        self.assertEqual(response.json["staffRoleLUTID"], 1)
        self.assertEqual(response.json["projectID"], 1)
        self.assertEqual(response.json["staffID"], 1)
        self.assertEqual(response.json["role"], 1)
        self.assertEqual(response.json["date_pledge"], "2016-02-02")
        self.assertEqual(response.json["date_revoked"], "2016-02-02")
        self.assertEqual(response.json["contact"], "yes")
        self.assertEqual(response.json["inactive"], "no")
        self.assertEqual(response.json["human_sub_training_exp"], "2016-02-02")
        self.assertEqual(response.json["human_sub_type_id"], 1)
        self.assertEqual(response.json["study_role"], 1)
        
    def test_update_staff(self):
        response = self.client.put("/api/projectstaff/1/", data = {
            "staffRoleLUTID" : 2,
            "projectID" : 2,
            "staffID" : 2,
            "role" : 2,
            "date_pledge" : "2016-02-03",
            "date_revoked" : "2016-02-03",
            "contact" : "no",
            "inactive" : "yes",
            "human_sub_training_exp" : "2016-02-03",
            "human_sub_type_id" : 2,
            "study_role" : 2
        })
        self.assertEqual(response.json["staffRoleLUTID"], 2)
        self.assertEqual(response.json["projectID"], 2)
        self.assertEqual(response.json["staffID"], 2)
        self.assertEqual(response.json["role"], 2)
        self.assertEqual(response.json["date_pledge"], "2016-02-03")
        self.assertEqual(response.json["date_revoked"], "2016-02-03")
        self.assertEqual(response.json["contact"], "no")
        self.assertEqual(response.json["inactive"], "yes")
        self.assertEqual(response.json["human_sub_training_exp"], "2016-02-03")
        self.assertEqual(response.json["human_sub_type_id"], 2)
        self.assertEqual(response.json["study_role"], 2)
        
    def test_delete_staff(self):
        response = self.client.delete("/api/projectstaff/1/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "ProjectStaffID 1 deleted")       
              
class TestProjectStatus(PopulatedDB):
    def test_get_project_statuses(self):
        response = self.client.get("/api/projectstatuses/")
        self.assertEqual(response.json["ProjectStatuses"][0]["projectStatusLUTID"], 1)
        self.assertEqual(response.json["ProjectStatuses"][0]["projectID"], 1)
        self.assertEqual(response.json["ProjectStatuses"][0]["staffID"], 1)
        self.assertEqual(response.json["ProjectStatuses"][0]["status_date"], "2016-02-02")
        self.assertEqual(response.json["ProjectStatuses"][0]["status_notes"], "notes")
        
    def test_get_project_status(self):
        response = self.client.get("/api/projectstatuses/1/")
        self.assertEqual(response.json["projectStatusLUTID"], 1)
        self.assertEqual(response.json["projectID"], 1)
        self.assertEqual(response.json["staffID"], 1)
        self.assertEqual(response.json["status_date"], "2016-02-02")
        self.assertEqual(response.json["status_notes"], "notes")
        
    def test_update_project_status(self):
        response = self.client.put("/api/projectstatuses/1/", data = {
            "projectStatusLUTID" : 2,
            "projectID": 2,
            "staffID" : 2,
            "status_date" : "2016-02-03",
            "status_notes": "notes Updated"
        })
        print(response.json)
        self.assertEqual(response.json["projectStatusLUTID"], 2)
        self.assertEqual(response.json["projectID"], 2)
        self.assertEqual(response.json["staffID"], 2)
        self.assertEqual(response.json["status_date"], "2016-02-03")
        self.assertEqual(response.json["status_notes"], "notes Updated")
        
    def test_delete_project_status(self):
        response = self.client.delete("/api/projectstatuses/1/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "ProjectStatusID 1 deleted")       
        
class TestProjectStatusType(PopulatedDB):
    def test_get_project_status_types(self):
        response = self.client.get("/api/projectstatustypes/")
        self.assertEqual(response.json["ProjectStatusTypes"][0]["projectStatusTypeID"], 1)
        self.assertEqual(response.json["ProjectStatusTypes"][0]["project_status"], "Status 1")
        self.assertEqual(response.json["ProjectStatusTypes"][0]["status_definition"], "status def")
        
    def test_get_project_status_type(self):
        response = self.client.get("/api/projectstatustypes/1/")
        self.assertEqual(response.json["projectStatusTypeID"], 1)
        self.assertEqual(response.json["project_status"], "Status 1")
        self.assertEqual(response.json["status_definition"], "status def")
        
    def test_update_project_status_type(self):
        response = self.client.put("/api/projectstatustypes/1/", data = {
            "project_status" : "Status 1 Updated",
            "status_definition" : "status def Updated"
        })
        self.assertEqual(response.json["projectStatusTypeID"], 1)
        self.assertEqual(response.json["project_status"], "Status 1 Updated")
        self.assertEqual(response.json["status_definition"], "status def Updated")
        
    def test_delete_project_status_type(self):
        response = self.client.delete("/api/projectstatustypes/1/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "ProjectStatusTypeID 1 deleted")            
 
class TestProjectType(PopulatedDB):
    def test_get_project_types(self):
        response = self.client.get("/api/projecttypes/")
        self.assertEqual(response.json["ProjectTypes"][0]["project_type"], "Type 1")
        self.assertEqual(response.json["ProjectTypes"][0]["project_type_definition"], "Def 1")
        
    def test_get_project_type(self):
        response = self.client.get("/api/projecttypes/1/")
        self.assertEqual(response.json["project_type"], "Type 1")
        self.assertEqual(response.json["project_type_definition"], "Def 1")
        
    def test_update_project_type(self):
        response = self.client.put("/api/projecttypes/1/", data = {
            "project_type" : "2",
            "project_type_definition" : "type def Updated"
        })
        self.assertEqual(response.json["project_type"], "2")
        self.assertEqual(response.json["project_type_definition"], "type def Updated")
        
    def test_delete_project_type(self):
        response = self.client.delete("/api/projecttypes/1/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "ProjectTypeID 1 deleted")      
 
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
        self.assertEqual(response.json["reviewCommitteeList"][0]["review_committee"], "rc")
        self.assertEqual(response.json["reviewCommitteeList"][0]["rc_description"], "rc desc")
        
    def test_get_review_committee_list(self):
        response = self.client.get("/api/reviewcommitteelist/1/")
        self.assertEqual(response.json["review_committee"], "rc")
        self.assertEqual(response.json["rc_description"], "rc desc")
        
    def test_update_review_committee_list(self):
        response = self.client.put("/api/reviewcommitteelist/1/", data = {
            "review_committee" : "rc Updated",
            "rc_description" : "rc desc Updated"
            })
        self.assertEqual(response.json["review_committee"],"rc Updated")
        self.assertEqual(response.json["rc_description"],"rc desc Updated")
        
    def test_delete_review_committee_list(self):
        response = self.client.delete("/api/reviewcommitteelist/1/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "RCListID 1 deleted")

class TestStaff(PopulatedDB):
    def test_get_staffs(self):
        response = self.client.get("/api/staff/")
        self.assertEqual(response.json["Staff"][0]["staffID"], 1)
        self.assertEqual(response.json["Staff"][0]["fname"], "fname")
        self.assertEqual(response.json["Staff"][0]["lname"], "lname")
        self.assertEqual(response.json["Staff"][0]["middle_name"], "middle_name")
        self.assertEqual(response.json["Staff"][0]["email"], "email")
        self.assertEqual(response.json["Staff"][0]["phone"], "phone")
        self.assertEqual(response.json["Staff"][0]["phoneComment"], "phoneComment")
        self.assertEqual(response.json["Staff"][0]["institution"], "institution")
        self.assertEqual(response.json["Staff"][0]["department"], "department")
        self.assertEqual(response.json["Staff"][0]["position"], "position")
        self.assertEqual(response.json["Staff"][0]["credentials"], "credentials")
        self.assertEqual(response.json["Staff"][0]["street"], "street")
        self.assertEqual(response.json["Staff"][0]["city"], "city")
        self.assertEqual(response.json["Staff"][0]["human_sub_training_exp"], "2016-02-02")
        self.assertEqual(response.json["Staff"][0]["UCR_role"], 1)

    def test_get_staff(self):
        response = self.client.get("/api/staff/1/")
        self.assertEqual(response.json["staffID"], 1)
        self.assertEqual(response.json["fname"], "fname")
        self.assertEqual(response.json["lname"], "lname")
        self.assertEqual(response.json["middle_name"], "middle_name")
        self.assertEqual(response.json["email"], "email")
        self.assertEqual(response.json["phone"], "phone")
        self.assertEqual(response.json["phoneComment"], "phoneComment")
        self.assertEqual(response.json["institution"], "institution")
        self.assertEqual(response.json["department"], "department")
        self.assertEqual(response.json["position"], "position")
        self.assertEqual(response.json["credentials"], "credentials")
        self.assertEqual(response.json["street"], "street")
        self.assertEqual(response.json["city"], "city")
        self.assertEqual(response.json["human_sub_training_exp"], "2016-02-02")
        self.assertEqual(response.json["UCR_role"], 1)
        
    def test_update_staff(self):
        response = self.client.put("/api/staff/1/", data = {
            "fname" : "fname2",
            "lname" : "lname2",
            "middle_name" : "middle_name2",
            "email" : "email2",
            "phone" : "phone2",
            "phoneComment" : "phoneComment2",
            "institution" : "institution2",
            "department" : "department2",
            "position" : "position2",
            "credentials" : "credentials2",
            "street" : "street2",
            "city" : "city2",
            "state" : "state2",
            "human_sub_training_exp" : "2016-02-03",
            "UCR_role" : 2
            })
        self.assertEqual(response.json["staffID"], 1)
        self.assertEqual(response.json["fname"], "fname2")
        self.assertEqual(response.json["lname"], "lname2")
        self.assertEqual(response.json["middle_name"], "middle_name2")
        self.assertEqual(response.json["email"], "email2")
        self.assertEqual(response.json["phone"], "phone2")
        self.assertEqual(response.json["phoneComment"], "phoneComment2")
        self.assertEqual(response.json["institution"], "institution2")
        self.assertEqual(response.json["department"], "department2")
        self.assertEqual(response.json["position"], "position2")
        self.assertEqual(response.json["credentials"], "credentials2")
        self.assertEqual(response.json["street"], "street2")
        self.assertEqual(response.json["city"], "city2")
        self.assertEqual(response.json["human_sub_training_exp"], "2016-02-03")
        self.assertEqual(response.json["UCR_role"], 2)
        
    def test_delete_staff(self):
        response = self.client.delete("/api/staff/1/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "StaffID 1 deleted")

class TestStaffRole(PopulatedDB):
    def test_get_staff_roles(self):
        response = self.client.get("/api/staffroles/")
        self.assertEqual(response.json["StaffRoles"][0]["staffRoleLUTID"], 1)
        self.assertEqual(response.json["StaffRoles"][0]["staffRole"], "role")
        self.assertEqual(response.json["StaffRoles"][0]["staffRoleDescription"], "desc")

    def test_get_staff_role(self):
        response = self.client.get("/api/staffroles/1/")
        self.assertEqual(response.json["staffRoleLUTID"], 1)
        self.assertEqual(response.json["staffRole"], "role")
        self.assertEqual(response.json["staffRoleDescription"], "desc")
        
    def test_update_staff_role(self):
        response = self.client.put("/api/staffroles/1/", data = {
            "staffRole" : "role Updated",
            "staffRoleDescription" : "desc Updated",
            })
        self.assertEqual(response.json["staffRoleLUTID"], 1)
        self.assertEqual(response.json["staffRole"], "role Updated")
        self.assertEqual(response.json["staffRoleDescription"], "desc Updated")
        
    def test_delete_staff_role(self):
        response = self.client.delete("/api/staffroles/1/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "StaffRoleLUTID 1 deleted")
           
class TestStaffTraining(PopulatedDB):
    def test_get_staff_trainings(self):
        response = self.client.get("/api/stafftrainings/")
        self.assertEqual(response.json["StaffTrainings"][0]["staffTrainingID"], 1)
        self.assertEqual(response.json["StaffTrainings"][0]["staffID"], 1)
        self.assertEqual(response.json["StaffTrainings"][0]["humanSubjectTrainingLUTID"], 1)
        self.assertEqual(response.json["StaffTrainings"][0]["date_taken"], "2016-02-02")
        self.assertEqual(response.json["StaffTrainings"][0]["exp_date"], "2016-02-02")

    def test_get_staff_training(self):
        response = self.client.get("/api/stafftrainings/1/")
        self.assertEqual(response.json["staffTrainingID"], 1)
        self.assertEqual(response.json["staffID"], 1)
        self.assertEqual(response.json["humanSubjectTrainingLUTID"], 1)
        self.assertEqual(response.json["date_taken"], "2016-02-02")
        self.assertEqual(response.json["exp_date"], "2016-02-02")
        
    def test_update_staff_training(self):
        response = self.client.put("/api/stafftrainings/1/", data = {
            "staffID" : 2,
            "humanSubjectTrainingLUTID" : 2,
            "date_taken" : "2016-02-03",
            "exp_date" : "2016-02-03"
            })
        self.assertEqual(response.json["staffTrainingID"], 1)
        self.assertEqual(response.json["staffID"], 2)
        self.assertEqual(response.json["humanSubjectTrainingLUTID"], 2)
        self.assertEqual(response.json["date_taken"], "2016-02-03")
        self.assertEqual(response.json["exp_date"], "2016-02-03")
        
    def test_delete_staff_training(self):
        response = self.client.delete("/api/stafftrainings/1/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "StaffTrainingID 1 deleted")
           
class TestTracing(PopulatedDB):
    def test_get_tracings(self):
        response = self.client.get("/api/tracings/")
        self.assertEqual(response.json["Tracings"][0]["tracingID"], 1)
        self.assertEqual(response.json["Tracings"][0]["tracingSourceLUTID"], 1)
        self.assertEqual(response.json["Tracings"][0]["projectPatientID"], 1)
        self.assertEqual(response.json["Tracings"][0]["date"], "2016-02-02")
        self.assertEqual(response.json["Tracings"][0]["staff"], 1)
        self.assertEqual(response.json["Tracings"][0]["notes"], "notes")
        
    def test_get_tracing(self):
        response = self.client.get("/api/tracings/1/")
        self.assertEqual(response.json["tracingID"], 1)
        self.assertEqual(response.json["tracingSourceLUTID"], 1)
        self.assertEqual(response.json["projectPatientID"], 1)
        self.assertEqual(response.json["date"], "2016-02-02")
        self.assertEqual(response.json["staff"], 1)
        self.assertEqual(response.json["notes"], "notes")
        
    def test_update_tracing(self):
        response = self.client.put("/api/tracings/1/", data = {
            "tracingSourceLUTID" : 2,
            "projectPatientID" : 2,
            "date" : "2016-02-03",
            "staff" : 2,
            "notes" : "notes Updated"
            })
        self.assertEqual(response.json["tracingID"], 1)
        self.assertEqual(response.json["tracingSourceLUTID"], 2)
        self.assertEqual(response.json["projectPatientID"], 2)
        self.assertEqual(response.json["date"], "2016-02-03")
        self.assertEqual(response.json["staff"], 2)
        self.assertEqual(response.json["notes"], "notes Updated")
        
    def test_delete_tracing(self):
        response = self.client.delete("/api/tracings/1/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "TracingID 1 deleted")
                     
class TestTracingSource(PopulatedDB):
    def test_get_tracing_sources(self):
        response = self.client.get("/api/tracingsources/")
        self.assertEqual(response.json["TracingSources"][0]["tracingSourceLUTID"], 1)
        self.assertEqual(response.json["TracingSources"][0]["description"], "desc")
        
    def test_get_tracing_source(self):
        response = self.client.get("/api/tracingsources/1/")
        self.assertEqual(response.json["tracingSourceLUTID"], 1)
        self.assertEqual(response.json["description"], "desc")
        
    def test_update_tracing_source(self):
        response = self.client.put("/api/tracingsources/1/", data = {
            "description" : "desc Updated"
            })
        self.assertEqual(response.json["tracingSourceLUTID"], 1)
        self.assertEqual(response.json["description"], "desc Updated")
        
    def test_delete_tracing_source(self):
        response = self.client.delete("/api/tracingsources/1/")
        self.assertEqual(response.json["Success"], True)
        self.assertEqual(response.json["Message"], "TracingSourceLUTID 1 deleted")
        
class TestUCRReport(PopulatedDB):
    def test_get_ucr_reports(self):
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