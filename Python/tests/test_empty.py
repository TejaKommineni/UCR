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
        return app.create_app(r'../tests/test_config.py')

    def setUp(self):
        db.drop_all()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def create_informant_relationships(self):
        relationships = []
        relationships.append(models.InformantRelationship(
            informantRelationship="Mother"
        ))
        relationships.append(models.InformantRelationship(
            informantRelationship="Father"
        ))
        relationships.append(models.InformantRelationship(
            informantRelationship="Son"
        ))
        relationships.append(models.InformantRelationship(
            informantRelationship="Daughter"
        ))
        relationships.append(models.InformantRelationship(
            informantRelationship="Grandson"
        ))
        relationships.append(models.InformantRelationship(
            informantRelationship="Granddaughter"
        ))
        relationships.append(models.InformantRelationship(
            informantRelationship="Uncle"
        ))
        relationships.append(models.InformantRelationship(
            informantRelationship="Aunt"
        ))
        relationships.append(models.InformantRelationship(
            informantRelationship="Cousin"
        ))
        relationships.append(models.InformantRelationship(
            informantRelationship="Wife"
        ))
        relationships.append(models.InformantRelationship(
            informantRelationship="Husband"
        ))
        relationships.append(models.InformantRelationship(
            informantRelationship="Friend"
        ))
        relationships.append(models.InformantRelationship(
            informantRelationship="Other Family Member"
        ))
        relationships.append(models.InformantRelationship(
            informantRelationship="Other"
        ))
        return relationships

    def create_final_codes(self):
        finalCodes = []
        finalCodes.append(models.FinalCode(
            finalCodeDefinition="Pending",
            finalCode=0
        ))
        finalCodes.append(models.FinalCode(
            finalCodeDefinition="Consent- Survey complete w/Med. Rcd. release",
            finalCode=100
        ))
        finalCodes.append(models.FinalCode(
            finalCodeDefinition="Consent- Survey complete NO Med.Rcd. release",
            finalCode=101
        ))
        finalCodes.append(models.FinalCode(
            finalCodeDefinition="Consent- Incomplete survey. Cannot complete (see notes for reason)",
            finalCode=111
        ))
        finalCodes.append(models.FinalCode(
            finalCodeDefinition="Survey complete- no consent form with or without medical release",
            finalCode=112
        ))
        finalCodes.append(models.FinalCode(
            finalCodeDefinition="No- by mail",
            finalCode=200
        ))
        finalCodes.append(models.FinalCode(
            finalCodeDefinition="No- no reason",
            finalCode=201

        ))
        finalCodes.append(models.FinalCode(
            finalCodeDefinition="No- too ill",
            finalCode=202
        ))
        finalCodes.append(models.FinalCode(
            finalCodeDefinition="No- no interest",
            finalCode=203
        ))
        finalCodes.append(models.FinalCode(
            finalCodeDefinition="No- too old",
            finalCode=204
        ))
        finalCodes.append(models.FinalCode(
            finalCodeDefinition="No- no cancer",
            finalCode=205
        ))
        finalCodes.append(models.FinalCode(
            finalCodeDefinition="No-upset",
            finalCode=207
        ))
        finalCodes.append(models.FinalCode(
            finalCodeDefinition="No- DO NOT CONTACT-per contact with patient on study",
            finalCode=208
        ))
        finalCodes.append(models.FinalCode(
            finalCodeDefinition="No- no signed consent form",
            finalCode=209
        ))
        finalCodes.append(models.FinalCode(
            finalCodeDefinition="No response after max effort",
            finalCode=300
        ))
        finalCodes.append(models.FinalCode(
            finalCodeDefinition="Lost to follow-up (bad/no address or phone)-may have contacted once or initial letter not returned, but can no longer contact",
            finalCode=301
        ))
        finalCodes.append(models.FinalCode(
            finalCodeDefinition="Language Barrier",
            finalCode=302
        ))
        finalCodes.append(models.FinalCode(
            finalCodeDefinition="No response after 2+ letters (no/bad phone)",
            finalCode=303
        ))
        finalCodes.append(models.FinalCode(
            finalCodeDefinition="Deceased AFTER selection",
            finalCode=309
        ))
        finalCodes.append(models.FinalCode(
            finalCodeDefinition="Ineligible - Current Age",
            finalCode=400
        ))
        finalCodes.append(models.FinalCode(
            finalCodeDefinition="Ineligible-other",
            finalCode=401
        ))
        finalCodes.append(models.FinalCode(
            finalCodeDefinition="Ineligible- DX date",
            finalCode=402
        ))
        finalCodes.append(models.FinalCode(
            finalCodeDefinition="Ineligible- Patient Deceased",
            finalCode=403
        ))
        finalCodes.append(models.FinalCode(
            finalCodeDefinition="Ineligible- mental capacity",
            finalCode=404
        ))
        finalCodes.append(models.FinalCode(
            finalCodeDefinition="Ineligible- histology or behavior",
            finalCode=406
        ))
        finalCodes.append(models.FinalCode(
            finalCodeDefinition="Ineligible- out of state resident at DX",
            finalCode=407
        ))
        finalCodes.append(models.FinalCode(
            finalCodeDefinition="Ineligible-Recently contacted for another UCR study or lost to follow-up in another UCR study within past year",
            finalCode=408
        ))
        finalCodes.append(models.FinalCode(
            finalCodeDefinition="Ineligible-out of country",
            finalCode=409
        ))
        finalCodes.append(models.FinalCode(
            finalCodeDefinition="Ineligible-Do not contact per DMS",
            finalCode=410
        ))
        finalCodes.append(models.FinalCode(
            finalCodeDefinition="Ineligible-Not able to send letter OR letter returned and no other contact possible (for NOK or Patient)",
            finalCode=411
        ))
        finalCodes.append(models.FinalCode(
            finalCodeDefinition="Ineligible - Contacted for other study within 1 year",
            finalCode=412
        ))
        finalCodes.append(models.FinalCode(
            finalCodeDefinition="Holding",
            finalCode=999
        ))
        return finalCodes

    def create_states(self):
        states = []
        states.append(models.State(
            state="Alabama"
        ))
        states.append(models.State(
            state="Alaska"
        ))
        states.append(models.State(
            state="Arizona"
        ))
        states.append(models.State(
            state="Arkansas"
        ))
        states.append(models.State(
            state="California"
        ))
        states.append(models.State(
            state="Colorado"
        ))
        states.append(models.State(
            state="Connecticut"
        ))
        states.append(models.State(
            state="Delaware"
        ))
        states.append(models.State(
            state="Florida"
        ))
        states.append(models.State(
            state="Georgia"
        ))
        states.append(models.State(
            state="Hawaii"
        ))
        states.append(models.State(
            state="Idaho"
        ))
        states.append(models.State(
            state="Illinois"
        ))
        states.append(models.State(
            state="Indiana"
        ))
        states.append(models.State(
            state="Iowa"
        ))
        states.append(models.State(
            state="Kansas"
        ))
        states.append(models.State(
            state="Kentucky"
        ))
        states.append(models.State(
            state="Louisiana"
        ))
        states.append(models.State(
            state="Maine"
        ))
        states.append(models.State(
            state="Maryland"
        ))
        states.append(models.State(
            state="Massachusetts"
        ))
        states.append(models.State(
            state="Michigan"
        ))
        states.append(models.State(
            state="Minnesota"
        ))
        states.append(models.State(
            state="Mississippi"
        ))
        states.append(models.State(
            state="Missouri"
        ))
        states.append(models.State(
            state="Montana"
        ))
        states.append(models.State(
            state="Nebraska"
        ))
        states.append(models.State(
            state="Nevada"
        ))
        states.append(models.State(
            state="New Hampshire"
        ))
        states.append(models.State(
            state="New Jersey"
        ))
        states.append(models.State(
            state="New Mexico"
        ))
        states.append(models.State(
            state="New York"
        ))
        states.append(models.State(
            state="North Carolina"
        ))
        states.append(models.State(
            state="North Dakota"
        ))
        states.append(models.State(
            state="Ohio"
        ))
        states.append(models.State(
            state="Oklahoma"
        ))
        states.append(models.State(
            state="Oregon"
        ))
        states.append(models.State(
            state="Pennsylvania"
        ))
        states.append(models.State(
            state="Rhhode Island"
        ))
        states.append(models.State(
            state="South Carolina"
        ))
        states.append(models.State(
            state="South Dakota"
        ))
        states.append(models.State(
            state="Tennessee"
        ))
        states.append(models.State(
            state="Texas"
        ))
        states.append(models.State(
            state="Utah"
        ))
        states.append(models.State(
            state="Vermont"
        ))
        states.append(models.State(
            state="Virginia"
        ))
        states.append(models.State(
            state="Washington"
        ))
        states.append(models.State(
            state="West Virginia"
        ))
        states.append(models.State(
            state="Wisonsin"
        ))
        states.append(models.State(
            state="Wyoming"
        ))
        states.append(models.State(
            state="District of Columbia"
        ))
        return states

    def create_abstract_statuses(self):
        statuses = []
        statuses.append(models.AbstractStatus(
            abstractStatus="Pending"
        ))
        statuses.append(models.AbstractStatus(
            abstractStatus="Eligible, Assigned to Abstractor"
        ))
        statuses.append(models.AbstractStatus(
            abstractStatus="Eligible, Received"
        ))
        statuses.append(models.AbstractStatus(
            abstractStatus="Complete"
        ))
        statuses.append(models.AbstractStatus(
            abstractStatus="Refused (no medical release)"
        ))
        statuses.append(models.AbstractStatus(
            abstractStatus="Not Included In Abstraction"
        ))
        return statuses

    def create_sexes(self):
        sexes = []
        sexes.append(models.Sex(
            sex="Female"
        ))
        sexes.append(models.Sex(
            sex="Male"
        ))
        sexes.append(models.Sex(
            sex="Transsexual"
        ))
        sexes.append(models.Sex(
            sex="Unknown"
        ))
        return sexes

    def create_races(self):
        races = []
        races.append(models.Race(
            race="American Indian or Alaska Native"
        ))
        races.append(models.Race(
            race="Asian"
        ))
        races.append(models.Race(
            race="Black"
        ))
        races.append(models.Race(
            race="Native Hawaiian or Other Pacific Islander"
        ))
        races.append(models.Race(
            race="White"
        ))
        races.append(models.Race(
            race="Unknown"
        ))
        return races

    def create_ethnicities(self):
        ethnicities = []
        ethnicities.append(models.Ethnicity(
            ethnicity="Hispanic or Latino"
        ))
        ethnicities.append(models.Ethnicity(
            ethnicity="Not Hispanic or Latino"
        ))
        ethnicities.append(models.Ethnicity(
            ethnicity="Unknown"
        ))
        return ethnicities

    def create_vital_statuses(self):
        vitals = []
        vitals.append(models.VitalStatus(
            vitalStatus="Alive"
        ))
        vitals.append(models.VitalStatus(
            vitalStatus="Dead"
        ))
        return vitals

    def create_contacts(self):
        contacts = []
        contacts.append(models.Contacts(
            contact="yes"
        ))
        contacts.append(models.Contacts(
            contact="no"
        ))
        return contacts

    def create_inactives(self):
        inactives = []
        inactives.append(models.Inactive(
            inactive="Yes"
        ))
        inactives.append(models.Inactive(
            inactive="No"
        ))
        return inactives

    def create_ucr_report_types(self):
        reports = []
        reports.append(models.UCRReportType(
            ucrReportType="Report 1"
        ))
        reports.append(models.UCRReportType(
            ucrReportType="Report 2"
        ))
        return reports

    def create_physician_statuses(self):
        statuses = []
        statuses.append(models.PhysicianStatus(
            physicianStatus="active"
        ))
        statuses.append(models.PhysicianStatus(
            physicianStatus="inactive"
        ))
        return statuses

    def create_physician_facility_statuses(self):
        statuses = []
        statuses.append(models.PhysicianFacilityStatus(
            physicianFacilityStatus="open"
        ))
        statuses.append(models.PhysicianFacilityStatus(
            physicianFacilityStatus="closed"
        ))
        return statuses

    def create_phone_types(self):
        phoneTypes = []
        phoneTypes.append(models.PhoneTypeLUT(
            phoneType="cell"
        ))
        phoneTypes.append(models.PhoneTypeLUT(
            phoneType="home"
        ))
        phoneTypes.append(models.PhoneTypeLUT(
            phoneType="work"
        ))
        return phoneTypes

    def create_irb_holders(self):
        holders = []
        holders.append(models.IRBHolderLUT(
            holder="U of U",
            holderDefinition="U of U researcher is responsible for IRB"
        ))
        holders.append(models.IRBHolderLUT(
            holder="External",
            holderDefinition="External researcher is responsible for IRB"
        ))
        holders.append(models.IRBHolderLUT(
            holder="UCR",
            holderDefinition="UCR is responsible for IRB. IRB is in UCR researcher's name"
        ))
        holders.append(models.IRBHolderLUT(
            holder="N/A",
            holderDefinition="Not Applicable"
        ))
        holders.append(models.IRBHolderLUT(
            holder="Unknown",
            holderDefinition="Unknown"
        ))
        holders.append(models.IRBHolderLUT(
            holder="Other",
            holderDefinition="Other"
        ))
        return holders

    def create_project_types(self):
        types = []
        types.append(models.ProjectType(
            projectType="Consent",
            projectTypeDefinition="UCR obtains patient consent for project"
        ))
        types.append(models.ProjectType(
            projectType="Permission",
            projectTypeDefinition="UCR obtains patient permission for project"
        ))
        types.append(models.ProjectType(
            projectType="Linkage",
            projectTypeDefinition="UCR conducts data linkage. No patient contact"
        ))
        types.append(models.ProjectType(
            projectType="Physician",
            projectTypeDefinition="UCR contacts physicians only. No patient contact."
        ))
        types.append(models.ProjectType(
            projectType="Other",
            projectTypeDefinition="Need to clean up"
        ))
        types.append(models.ProjectType(
            projectType="Unknown",
            projectTypeDefinition="When still in application phase"
        ))
        types.append(models.ProjectType(
            projectType="Tumor",
            projectTypeDefinition="UCR creates a tumor level data file.  No patient contact. No linkage conducted"
        ))
        return types

    def create_contact_statuses(self):
        contactInfoStatuses = []
        contactInfoStatuses.append(models.ContactInfoStatusLUT(
            contactInfoStatus="Current"
        ))
        contactInfoStatuses.append(models.ContactInfoStatusLUT(
            contactInfoStatus="Unknown"
        ))
        contactInfoStatuses.append(models.ContactInfoStatusLUT(
            contactInfoStatus="Bad"
        ))
        contactInfoStatuses.append(models.ContactInfoStatusLUT(
            contactInfoStatus="Duplicate"
        ))
        return contactInfoStatuses

    def create_contact_sources(self):
        contactSources = []
        contactSources.append(models.ContactInfoSourceLUT(
            contactInfoSource="UCR"
        ))
        contactSources.append(models.ContactInfoSourceLUT(
            contactInfoSource="UPDB"
        ))
        contactSources.append(models.ContactInfoSourceLUT(
            contactInfoSource="Patient or NOK"
        ))
        contactSources.append(models.ContactInfoSourceLUT(
            contactInfoSource="Research"
        ))
        contactSources.append(models.ContactInfoSourceLUT(
            contactInfoSource="USPS"
        ))
        contactSources.append(models.ContactInfoSourceLUT(
            contactInfoSource="Bad"
        ))
        contactSources.append(models.ContactInfoSourceLUT(
            contactInfoSource="Accurint"
        ))
        return contactSources

    def create_grant_statuses(self):
        statuses = []
        statuses.append(models.GrantStatusLUT(
            grantStatus="Submitted"
        ))
        statuses.append(models.GrantStatusLUT(
            grantStatus="Awarded"
        ))
        statuses.append(models.GrantStatusLUT(
            grantStatus="Rejected"
        ))
        return statuses

    def create_funding_sources(self):
        sources = []
        sources.append(models.FundingSourceLUT(
            fundingSource="NCI"
        ))
        sources.append(models.FundingSourceLUT(
            fundingSource="NCI-Pilot"
        ))
        sources.append(models.FundingSourceLUT(
            fundingSource="U of U Department"
        ))
        sources.append(models.FundingSourceLUT(
            fundingSource="SEER"
        ))
        sources.append(models.FundingSourceLUT(
            fundingSource="UDOH"
        ))
        sources.append(models.FundingSourceLUT(
            fundingSource="AHRQ"
        ))
        sources.append(models.FundingSourceLUT(
            fundingSource="PCORI"
        ))
        sources.append(models.FundingSourceLUT(
            fundingSource="CHOICE"
        ))
        sources.append(models.FundingSourceLUT(
            fundingSource="Private Industry"
        ))
        sources.append(models.FundingSourceLUT(
            fundingSource="NIH"
        ))
        sources.append(models.FundingSourceLUT(
            fundingSource="Primary Children's Hospital Foundation"
        ))
        sources.append(models.FundingSourceLUT(
            fundingSource="United BioSource Corporation"
        ))
        sources.append(models.FundingSourceLUT(
            fundingSource="Novo Nordisk"
        ))
        sources.append(models.FundingSourceLUT(
            fundingSource="RTI"
        ))
        return sources

    def create_review_committee_statuses(self):
        statuses = []
        statuses.append(models.ReviewCommitteeStatusLUT(
            reviewCommitteeStatus="Pending",
            reviewCommitteeStatusDefinition="Pending"
        ))
        statuses.append(models.ReviewCommitteeStatusLUT(
            reviewCommitteeStatus="Approved",
            reviewCommitteeStatusDefinition="Approved"
        ))
        statuses.append(models.ReviewCommitteeStatusLUT(
            reviewCommitteeStatus="Closed",
            reviewCommitteeStatusDefinition="Closed"
        ))
        statuses.append(models.ReviewCommitteeStatusLUT(
            reviewCommitteeStatus="Non Human Subject",
            reviewCommitteeStatusDefinition="Non Human Subject"
        ))
        statuses.append(models.ReviewCommitteeStatusLUT(
            reviewCommitteeStatus="Exempt",
            reviewCommitteeStatusDefinition="Exempt"
        ))
        statuses.append(models.ReviewCommitteeStatusLUT(
            reviewCommitteeStatus="Signed",
            reviewCommitteeStatusDefinition="Signed"
        ))
        statuses.append(models.ReviewCommitteeStatusLUT(
            reviewCommitteeStatus="Sent - Carol",
            reviewCommitteeStatusDefinition="Sent - Carol"
        ))
        statuses.append(models.ReviewCommitteeStatusLUT(
            reviewCommitteeStatus="Not Needed",
            reviewCommitteeStatusDefinition="Not Needed"
        ))
        statuses.append(models.ReviewCommitteeStatusLUT(
            reviewCommitteeStatus="Sent - Full ARC Review",
            reviewCommitteeStatusDefinition="Sent - Full ARC Review"
        ))
        statuses.append(models.ReviewCommitteeStatusLUT(
            reviewCommitteeStatus="Unknown",
            reviewCommitteeStatusDefinition="Unknown"
        ))
        statuses.append(models.ReviewCommitteeStatusLUT(
            reviewCommitteeStatus="Expired",
            reviewCommitteeStatusDefinition="Expired"
        ))
        statuses.append(models.ReviewCommitteeStatusLUT(
            reviewCommitteeStatus="Submitted",
            reviewCommitteeStatusDefinition="Submitted"
        ))
        return statuses

    def create_project_statuses(self):
        statuses = []
        statuses.append(models.ProjectStatusLUT(
            projectStatus="Pending",
            projectStatusDefinition="Project has not started"
        ))
        statuses.append(models.ProjectStatusLUT(
            projectStatus="Active",
            projectStatusDefinition="Project is underway"
        ))
        statuses.append(models.ProjectStatusLUT(
            projectStatus="Hibernate",
            projectStatusDefinition="Project has open IRB, but no current UCR activity"
        ))
        statuses.append(models.ProjectStatusLUT(
            projectStatus="IRB Closed",
            projectStatusDefinition="IRB is closed. Project is closed."
        ))
        statuses.append(models.ProjectStatusLUT(
            projectStatus="Archived",
            projectStatusDefinition="Project is old and inactive for years. IRB is closed."
        ))
        statuses.append(models.ProjectStatusLUT(
            projectStatus="Canceled",
            projectStatusDefinition="Project never materialized."
        ))
        statuses.append(models.ProjectStatusLUT(
            projectStatus="Pre-Application",
            projectStatusDefinition="Received pre-application"
        ))
        statuses.append(models.ProjectStatusLUT(
            projectStatus="Application",
            projectStatusDefinition="Application under review"
        ))
        statuses.append(models.ProjectStatusLUT(
            projectStatus="Post-Contact",
            projectStatusDefinition="Only for contact studies: Contact complete but we are still reviewing pubs and/or linking data."
        ))
        statuses.append(models.ProjectStatusLUT(
            projectStatus="Linkage",
            projectStatusDefinition="Regularly Scheduled Linkages"
        ))
        return statuses

    def create_log_subjects(self):
        subjects = []
        subjects.append(models.LogSubjectLUT(
            logSubject="Review Committee"
        ))
        subjects.append(models.LogSubjectLUT(
            logSubject="Budget"
        ))
        subjects.append(models.LogSubjectLUT(
            logSubject="Misc."
        ))
        subjects.append(models.LogSubjectLUT(
            logSubject="Data"
        ))
        subjects.append(models.LogSubjectLUT(
            logSubject="Pre-Application"
        ))
        subjects.append(models.LogSubjectLUT(
            logSubject="Application"
        ))
        subjects.append(models.LogSubjectLUT(
            logSubject="Recruitment"
        ))
        subjects.append(models.LogSubjectLUT(
            logSubject="Audit"
        ))
        subjects.append(models.LogSubjectLUT(
            logSubject="Start-up"
        ))
        subjects.append(models.LogSubjectLUT(
            logSubject="Publication"
        ))
        subjects.append(models.LogSubjectLUT(
            logSubject="Close-out"
        ))
        subjects.append(models.LogSubjectLUT(
            logSubject="Agreements"
        ))
        subjects.append(models.LogSubjectLUT(
            logSubject="Reports"
        ))
        return subjects

    def create_review_committees(self):
        rcs = []
        rcs.append(models.ReviewCommitteeLUT(
            reviewCommittee="U of U IRB",
            reviewCommitteeDescription=None
        ))
        rcs.append(models.ReviewCommitteeLUT(
            reviewCommittee="ARC",
            reviewCommitteeDescription=None
        ))
        rcs.append(models.ReviewCommitteeLUT(
            reviewCommittee="IHC",
            reviewCommitteeDescription=None
        ))
        rcs.append(models.ReviewCommitteeLUT(
            reviewCommittee="St Marks",
            reviewCommitteeDescription=None
        ))
        rcs.append(models.ReviewCommitteeLUT(
            reviewCommittee="Odgen",
            reviewCommitteeDescription=None
        ))
        rcs.append(models.ReviewCommitteeLUT(
            reviewCommittee="IASIS",
            reviewCommitteeDescription=None
        ))
        rcs.append(models.ReviewCommitteeLUT(
            reviewCommittee="Vanderbuilt",
            reviewCommitteeDescription=None
        ))
        rcs.append(models.ReviewCommitteeLUT(
            reviewCommittee="Emory",
            reviewCommitteeDescription=None
        ))
        rcs.append(models.ReviewCommitteeLUT(
            reviewCommittee="UCR Admin",
            reviewCommitteeDescription=None
        ))
        rcs.append(models.ReviewCommitteeLUT(
            reviewCommittee="RTI",
            reviewCommitteeDescription=None
        ))
        rcs.append(models.ReviewCommitteeLUT(
            reviewCommittee="Loma Linda University",
            reviewCommitteeDescription=None
        ))
        rcs.append(models.ReviewCommitteeLUT(
            reviewCommittee="NCI-CDA",
            reviewCommitteeDescription=None
        ))
        rcs.append(models.ReviewCommitteeLUT(
            reviewCommittee="Sterling",
            reviewCommitteeDescription=None
        ))
        rcs.append(models.ReviewCommitteeLUT(
            reviewCommittee="UCR Research Agreement",
            reviewCommitteeDescription="Expires after 5 years"
        ))
        rcs.append(models.ReviewCommitteeLUT(
            reviewCommittee="UCR Research Application",
            reviewCommitteeDescription="Renewed annually"
        ))
        rcs.append(models.ReviewCommitteeLUT(
            reviewCommittee="UCR Annual Report",
            reviewCommitteeDescription="Annually"
        ))
        rcs.append(models.ReviewCommitteeLUT(
            reviewCommittee="UCR Research Proposal",
            reviewCommitteeDescription=None
        ))
        rcs.append(models.ReviewCommitteeLUT(
            reviewCommittee="RGE",
            reviewCommitteeDescription=None
        ))
        rcs.append(models.ReviewCommitteeLUT(
            reviewCommittee="Westat",
            reviewCommitteeDescription=None
        ))
        rcs.append(models.ReviewCommitteeLUT(
            reviewCommittee="UDOH Data Use Committees",
            reviewCommitteeDescription=None
        ))
        rcs.append(models.ReviewCommitteeLUT(
            reviewCommittee="OHSRP - NIH Office of Human Subjects Research",
            reviewCommitteeDescription=None
        ))
        rcs.append(models.ReviewCommitteeLUT(
            reviewCommittee="UDOH IRB",
            reviewCommitteeDescription=None
        ))
        rcs.append(models.ReviewCommitteeLUT(
            reviewCommittee="UDOH Health Data Committee",
            reviewCommitteeDescription=None
        ))
        return rcs

    def create_staff_roles(self):
        roles = []
        roles.append(models.StaffRoleLUT(
            staffRole="PI-External",
            staffRoleDescription="Principle Investigator- external, no U of U affiliation"
        ))
        roles.append(models.StaffRoleLUT(
            staffRole="Co-PI",
            staffRoleDescription="Co-PI"
        ))
        roles.append(models.StaffRoleLUT(
            staffRole="Coordinator",
            staffRoleDescription="Runs study for investigator"
        ))
        roles.append(models.StaffRoleLUT(
            staffRole="Research Assistant",
            staffRoleDescription="Assists on study"
        ))
        roles.append(models.StaffRoleLUT(
            staffRole="Research Associate",
            staffRoleDescription=None
        ))
        roles.append(models.StaffRoleLUT(
            staffRole="UCR Staff",
            staffRoleDescription=None
        ))
        roles.append(models.StaffRoleLUT(
            staffRole="Data Analyst",
            staffRoleDescription=None
        ))
        roles.append(models.StaffRoleLUT(
            staffRole="PI-U of U",
            staffRoleDescription="Principle Investigator- U of U affiliation"
        ))
        roles.append(models.StaffRoleLUT(
            staffRole="PI-UCR",
            staffRoleDescription="Principle Investigator- UCR Researcher"
        ))
        roles.append(models.StaffRoleLUT(
            staffRole="PPR Staff",
            staffRoleDescription="UPDB Staff"
        ))
        roles.append(models.StaffRoleLUT(
            staffRole="Programmer",
            staffRoleDescription=None
        ))
        roles.append(models.StaffRoleLUT(
            staffRole="Adminstrative Staff",
            staffRoleDescription="No access to confidential data manages budget etc."
        ))
        return roles

    def create_project_phases(self):
        phases = []
        phases.append(models.PhaseStatus(
            phaseStatus="Received",
            phaseDescription="Items received from investigator"
        ))
        phases.append(models.PhaseStatus(
            phaseStatus="Meeting Scheduled",
            phaseDescription=None
        ))
        phases.append(models.PhaseStatus(
            phaseStatus="In Review",
            phaseDescription=None
        ))
        phases.append(models.PhaseStatus(
            phaseStatus="ARC Approved",
            phaseDescription=None
        ))
        phases.append(models.PhaseStatus(
            phaseStatus="Sent to ARC",
            phaseDescription=None
        ))
        phases.append(models.PhaseStatus(
            phaseStatus="Sent to Carol",
            phaseDescription=None
        ))
        phases.append(models.PhaseStatus(
            phaseStatus="Sent to Investigator",
            phaseDescription=None
        ))
        phases.append(models.PhaseStatus(
            phaseStatus="Contract Signed",
            phaseDescription=None
        ))
        phases.append(models.PhaseStatus(
            phaseStatus="SOP Complete",
            phaseDescription=None
        ))
        phases.append(models.PhaseStatus(
            phaseStatus="IRB Approval",
            phaseDescription=None
        ))
        phases.append(models.PhaseStatus(
            phaseStatus="RGE Approval",
            phaseDescription=None
        ))
        phases.append(models.PhaseStatus(
            phaseStatus="Annual Review Received",
            phaseDescription=None
        ))
        phases.append(models.PhaseStatus(
            phaseStatus="Notified Carrie Database Needed",
            phaseDescription=None
        ))
        phases.append(models.PhaseStatus(
            phaseStatus="Project Lead Assigned",
            phaseDescription=None
        ))
        phases.append(models.PhaseStatus(
            phaseStatus="Project Lead Assigned",
            phaseDescription=None
        ))
        phases.append(models.PhaseStatus(
            phaseStatus="Study Complete",
            phaseDescription=None
        ))
        phases.append(models.PhaseStatus(
            phaseStatus="Meeting",
            phaseDescription=None
        ))
        phases.append(models.PhaseStatus(
            phaseStatus="Invoice Sent",
            phaseDescription=None
        ))
        phases.append(models.PhaseStatus(
            phaseStatus="Data Transfer",
            phaseDescription=None
        ))
        phases.append(models.PhaseStatus(
            phaseStatus="Report to Researcher",
            phaseDescription=None
        ))
        phases.append(models.PhaseStatus(
            phaseStatus="Approved/Agreed",
            phaseDescription=None
        ))
        phases.append(models.PhaseStatus(
            phaseStatus="Email/Phone from CRO",
            phaseDescription=None
        ))
        phases.append(models.PhaseStatus(
            phaseStatus="IRB Continuing Review",
            phaseDescription=None
        ))
        phases.append(models.PhaseStatus(
            phaseStatus="OSP",
            phaseDescription=None
        ))
        phases.append(models.PhaseStatus(
            phaseStatus="Study Activities",
            phaseDescription=None
        ))
        phases.append(models.PhaseStatus(
            phaseStatus="Accounting",
            phaseDescription=None
        ))
        phases.append(models.PhaseStatus(
            phaseStatus="IRB Amendment",
            phaseDescription=None
        ))
        phases.append(models.PhaseStatus(
            phaseStatus="Email",
            phaseDescription=None
        ))
        phases.append(models.PhaseStatus(
            phaseStatus="Report In Progress",
            phaseDescription=None
        ))
        phases.append(models.PhaseStatus(
            phaseStatus="Report Sent",
            phaseDescription=None
        ))
        phases.append(models.PhaseStatus(
            phaseStatus="IRB Submitted",
            phaseDescription=None
        ))
        return phases

    def create_human_subject_trainings(self):
        hsts = []
        hsts.append(models.HumanSubjectTrainingLUT(
            trainingType="CITI"
        ))
        hsts.append(models.HumanSubjectTrainingLUT(
            trainingType="NIH"
        ))
        hsts.append(models.HumanSubjectTrainingLUT(
            trainingType="VA"
        ))
        hsts.append(models.HumanSubjectTrainingLUT(
            trainingType="Unknown"
        ))
        hsts.append(models.HumanSubjectTrainingLUT(
            trainingType="N/A"
        ))
        return hsts

    def create_tracing_sources(self):
        sources = []
        sources.append(models.TracingSourceLUT(
            description="DMS"
        ))
        sources.append(models.TracingSourceLUT(
            description="Filer4"
        ))
        sources.append(models.TracingSourceLUT(
            description="DEX/White pages"
        ))
        sources.append(models.TracingSourceLUT(
            description="Intellus"
        ))
        sources.append(models.TracingSourceLUT(
            description="Dr Office"
        ))
        sources.append(models.TracingSourceLUT(
            description="Voter DB"
        ))
        sources.append(models.TracingSourceLUT(
            description="Zaba"
        ))
        sources.append(models.TracingSourceLUT(
            description="Other (Enter in Notes)"
        ))
        sources.append(models.TracingSourceLUT(
            description="Obit"
        ))
        sources.append(models.TracingSourceLUT(
            description="Advance Bkground Check"
        ))
        return sources

    def create_contact_types(self):
        contact_types = []
        contact_types.append(models.ContactTypeLUT(
            contactDefinition="Mailed 1st packet to patient (intro letter, survey, consent, med rcd. release)",
            contactCode=100
        ))
        contact_types.append(models.ContactTypeLUT(
            contactDefinition="Mailed Reminder letter",
            contactCode=101
        ))
        contact_types.append(models.ContactTypeLUT(
            contactDefinition="Mailed 2nd packet (FU letter, survey, consent, med rcd release)",
            contactCode=102
        ))
        contact_types.append(models.ContactTypeLUT(
            contactDefinition="Mailed Thank you letter and copy of consent form",
            contactCode=103
        ))
        contact_types.append(models.ContactTypeLUT(
            contactDefinition="Mailed Packet (after phone contact)",
            contactCode=109
        ))
        contact_types.append(models.ContactTypeLUT(
            contactDefinition="Mailed additional items- (survey, consent form, envelope, etc)",
            contactCode=110
        ))
        contact_types.append(models.ContactTypeLUT(
            contactDefinition="Undeliverable, mail returned w/forwarding addresses, mailed to new address",
            contactCode=150
        ))
        contact_types.append(models.ContactTypeLUT(
            contactDefinition="Undeliverable, Mail returned, NO forwarding address",
            contactCode=151
        ))
        contact_types.append(models.ContactTypeLUT(
            contactDefinition="Packet Returned - Temporarily Away",
            contactCode=152
        ))
        contact_types.append(models.ContactTypeLUT(
            contactDefinition="Left voicemail",
            contactCode=200
        ))
        contact_types.append(models.ContactTypeLUT(
            contactDefinition="Left message with person",
            contactCode=201
        ))
        contact_types.append(models.ContactTypeLUT(
            contactDefinition="No answer",
            contactCode=202
        ))
        contact_types.append(models.ContactTypeLUT(
            contactDefinition="Busy",
            contactCode=203
        ))
        contact_types.append(models.ContactTypeLUT(
            contactDefinition="Bad Phone number",
            contactCode=204
        ))
        contact_types.append(models.ContactTypeLUT(
            contactDefinition="Spoke with- Received, thinking about it",
            contactCode=205
        ))
        contact_types.append(models.ContactTypeLUT(
            contactDefinition="Spoke with- Received, willing",
            contactCode=206
        ))
        contact_types.append(models.ContactTypeLUT(
            contactDefinition="Spoke with- Received, already sent to us",
            contactCode=207
        ))
        contact_types.append(models.ContactTypeLUT(
            contactDefinition="Spoke with- too sick",
            contactCode=208
        ))
        contact_types.append(models.ContactTypeLUT(
            contactDefinition="Spoke with- no cancer",
            contactCode=209
        ))
        contact_types.append(models.ContactTypeLUT(
            contactDefinition="Language Barrier",
            contactCode=210
        ))
        contact_types.append(models.ContactTypeLUT(
            contactDefinition="Deceased",
            contactCode=211
        ))
        contact_types.append(models.ContactTypeLUT(
            contactDefinition="Pt unable to come to phone, could not leave message",
            contactCode=212
        ))
        contact_types.append(models.ContactTypeLUT(
            contactDefinition="Incompetent",
            contactCode=213
        ))
        contact_types.append(models.ContactTypeLUT(
            contactDefinition="Patient left message for Coordinator",
            contactCode=214
        ))
        contact_types.append(models.ContactTypeLUT(
            contactDefinition="Spoke with- Refused (no reason given)",
            contactCode=215
        ))
        contact_types.append(models.ContactTypeLUT(
            contactDefinition="Ineligible",
            contactCode=216
        ))
        contact_types.append(models.ContactTypeLUT(
            contactDefinition="Spoke with- did not receive, mailed another letter",
            contactCode=217
        ))
        contact_types.append(models.ContactTypeLUT(
            contactDefinition="Spoke with- Other",
            contactCode=218
        ))
        contact_types.append(models.ContactTypeLUT(
            contactDefinition="Survey returned without consent form",
            contactCode=300
        ))
        contact_types.append(models.ContactTypeLUT(
            contactDefinition="Survey returned incomplete",
            contactCode=301
        ))
        contact_types.append(models.ContactTypeLUT(
            contactDefinition="Consent returned without survey",
            contactCode=302
        ))
        contact_types.append(models.ContactTypeLUT(
            contactDefinition="Received consent, survey received previously",
            contactCode=304
        ))
        contact_types.append(models.ContactTypeLUT(
            contactDefinition="Enter in error",
            contactCode=999
        ))
        return contact_types

    def create_ucr_roles(self):
        roles = []
        roles.append(models.UCRRole(
            ucrRole="role 1"
        ))
        return roles

    def create_gift_cards(self):
        gcs = []
        gcs.append(models.GiftCard(
            description="Smiths Gift Card",
            barcode="123456789",
            amount=25
        ))
        gcs.append(models.GiftCard(
            description="Smiths Gift Card",
            barcode="123456788",
            amount=25
        ))
        gcs.append(models.GiftCard(
            description="Smiths Gift Card",
            barcode="123456787",
            amount=25
        ))
        return gcs

    def create_roles(self):
        roles = []
        roles.append(models.Role(
            role="Contact Staff"
        ))
        roles.append(models.Role(
            role="Developer"
        ))
        roles.append(models.Role(
            role="Director"
        ))
        roles.append(models.Role(
            role="Informatics Staff"
        ))
        roles.append(models.Role(
            role="Research Manager"
        ))
        return roles

    def create_users(self):
        users = []
        users.append(models.User(
            uID="u0973461",
            roleID=2  # developer
        ))
        users.append(models.User(
            uID="u0050151",
            roleID=1  # Contact Staff
        ))
        return users

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

class TestAbstractStatuses(BlankDB):

    def test_empty_abstract_statuses(self):
        response = self.client.get("/api/abstractstatuses/")
        self.assertEqual(response.json, {"abstractStatuses" : []})

    def test_abstract_status_no_id(self):
        response = self.client.get("/api/abstractstatuses/1/")
        self.assertEqual(response.json, {"Error" : "AbstractStatusID 1 not found"})

    def test_create_abstract_status(self):
        response = self.client.post("/api/abstractstatuses/", data={
            "abstractStatus": "status"
        })
        self.assertEqual(response.json["abstractStatusID"], 1)
        self.assertEqual(response.json["abstractStatus"], "status")

class TestArcReview(BlankDB):
    def setUp(self):
        db.drop_all()
        db.create_all()
        self.populate_db()

    def populate_db(self):
        # Need to populate the FK tables with stuff
        pt1 = models.ProjectType(
            projectType="Consent",
            projectTypeDefinition="UCR obtains patient consent for project")

        irb_holder1 = models.IRBHolderLUT(
            holder="U of U",
            holderDefinition="U of U researcher is responsible for IRB")

        p = models.Project(
            projectTypeID=1,
            irbHolderID=1,
            projectTitle="Test Project",
            shortTitle="Test Project",
            projectSummary="Summary",
            sop="sop",
            ucrProposal="ucr_proposal",
            budgetDoc="budget_doc",
            ucrFee="no",
            ucrNoFee="yes",
            previousShortTitle="t short",
            dateAdded=datetime(2016, 2, 2),
            finalRecruitmentReport="report",
            ongoingContact=True,
            activityStartDate=datetime(2016, 2, 2),
            activityEndDate=datetime(2016, 2, 2))

        p.irbHolder = irb_holder1
        p.projectType = pt1
        db.session.add(p)
        db.session.commit()

    def test_empty_arc_review(self):
        response = self.client.get("/api/arcreviews/")
        self.assertEqual(response.json, {"arcReviews" : []})
        
    def test_arc_review_no_id(self):
        response = self.client.get("/api/arcreviews/1/")
        self.assertEqual(response.json, {"Error" : "ArcReviewID 1 not found"})
    
    def test_create_arc_review(self):
        response = self.client.post("/api/arcreviews/", data = {
            "projectID" : 1,
            "reviewType" : 1,
            "dateSentToReviewer" : "2016-02-02",
            "reviewer1" : 1,
            "reviewer1Rec" : 1,
            "reviewer1SigDate" : "2016-02-02",
            "reviewer1Comments" : "comments",
            "reviewer2" : 2,
            "reviewer2Rec"  :2 ,
            "reviewer2SigDate" : "2016-02-02",
            "reviewer2Comments" : "comments",
            "research" : 1,
            "linkage": "false",
            "contact" : "false",
            "engaged" : "false",
            "nonPublicData" : "false",
            "versionID" : 1,
        })
        self.assertEqual(response.json["arcReviewID"], 1)
        self.assertEqual(response.json["projectID"], 1)
        self.assertEqual(response.json["reviewType"], 1)
        self.assertEqual(response.json["dateSentToReviewer"], "2016-02-02")
        self.assertEqual(response.json["reviewer1"], 1)
        self.assertEqual(response.json["reviewer1Rec"], 1)
        self.assertEqual(response.json["reviewer1SigDate"], "2016-02-02")
        self.assertEqual(response.json["reviewer1Comments"], "comments")
        self.assertEqual(response.json["reviewer2"], 2)
        self.assertEqual(response.json["reviewer2Rec"], 2)
        self.assertEqual(response.json["reviewer2SigDate"], "2016-02-02")
        self.assertEqual(response.json["reviewer2Comments"], "comments")
        self.assertEqual(response.json["research"], 1)
        self.assertEqual(response.json["linkage"], False)
        self.assertEqual(response.json["contact"], False)
        self.assertEqual(response.json["engaged"], False)
        self.assertEqual(response.json["nonPublicData"], False)
        self.assertEqual(response.json["versionID"], 1)

class TestBudget(BlankDB):
    def setUp(self):
        db.drop_all()
        db.create_all()
        self.populate_db()

    def populate_db(self):
        # Need to populate the FK tables with stuff
        pt1 = models.ProjectType(
            projectType="Consent",
            projectTypeDefinition="UCR obtains patient consent for project")

        irb_holder1 = models.IRBHolderLUT(
            holder="U of U",
            holderDefinition="U of U researcher is responsible for IRB")

        p = models.Project(
            projectTypeID=1,
            irbHolderID=1,
            projectTitle="Test Project",
            shortTitle="Test Project",
            projectSummary="Summary",
            sop="sop",
            ucrProposal="ucr_proposal",
            budgetDoc="budget_doc",
            ucrFee="no",
            ucrNoFee="yes",
            previousShortTitle="t short",
            dateAdded=datetime(2016, 2, 2),
            finalRecruitmentReport="report",
            ongoingContact=True,
            activityStartDate=datetime(2016, 2, 2),
            activityEndDate=datetime(2016, 2, 2))

        p.irbHolder = irb_holder1
        p.projectType = pt1
        db.session.add(p)
        db.session.commit()

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
            "periodComment" : "comment",
            "versionID" : 1,
        })
        self.assertEqual(response.json["budgetID"], 1)
        self.assertEqual(response.json["numPeriods"], 2)
        self.assertEqual(response.json["periodStart"], "2016-02-02")
        self.assertEqual(response.json["periodEnd"], "2016-02-02")
        self.assertEqual(response.json["periodComment"], "comment")
        self.assertEqual(response.json["versionID"], 1)

class TestContact(BlankDB):
    def setUp(self):
        db.drop_all()
        db.create_all()
        self.populate_db()

    def populate_db(self):
        facility1 = models.Facility(
            facilityName = "name",
            contactFirstName = "fname",
            contactLastName = "lname",
            facilityStatus = 1,
            facilityStatusDate = datetime(2016,2,2),
            contact2FirstName = "fname",
            contact2LastName = "lname"
        )
        patient = models.Patient(
            patID="1",
            ucrDistID=1,
            UPDBID=1,
            firstName="fname2",
            lastName="lname2",
            middleName="mname2",
            maidenName="maiden_name",
            aliasFirstName="alias_fname",
            aliasLastName="alias_lname",
            aliasMiddleName="alias_middle",
            dobDay=26,
            dobMonth=4,
            dobYear=1970,
            SSN="999999999",
            sexID=1,
            raceID=2,
            ethnicityID=1,
            vitalStatusID=2
        )

        facilityPhone = models.FacilityPhone(
            contactInfoSourceID=1,
            facilityID=1,
            contactInfoStatusID=1,
            clinicName="clinic",
            phoneTypeID=1,
            phoneNumber="phone",
            phoneStatusDate=datetime(2016, 2, 2)
        )

        informant = models.Informant(
            participantID=1,
            firstName="fname",
            lastName="lname",
            middleName="middle_name",
            informantPrimary="informant_primary",
            informantRelationship="informant_relationship",
            notes="notes"
        )

        informantPhone = models.InformantPhone(
            contactInfoSourceID=1,
            informantID=1,
            contactInfoStatusID=1,
            phoneTypeID=1,
            phoneNumber="phone",
            phoneStatusDate=datetime(2016, 2, 2)
        )

        physician = models.Physician(
            firstName="fname",
            lastName="lname",
            middleName="middle_name",
            credentials="credentials",
            specialty="specialty",
            aliasFirstName="alias_fname",
            aliasLastName="alias_lname",
            aliasMiddleName="alias_middle_name",
            physicianStatusID=1,
            physicianStatusDate=datetime(2016, 2, 2),
        )
        physicianPhone = models.PhysicianPhone(
            contactInfoSourceID=1,
            physicianID=1,
            contactInfoStatusID=1,
            phoneNumber="phone",
            phoneTypeID=1,
            phoneStatusDate=datetime(2016, 2, 2)
        )

        patientPhone = models.PatientPhone(
            contactInfoSourceID=1,
            participantID=1,
            contactInfoStatusID=1,
            phoneTypeID=1,
            phoneNumber="phone",
            phoneStatusDate=datetime(2016, 2, 2)
        )

        project1 = models.Project(
            projectTypeID=1,
            irbHolderID=1,
            projectTitle="Test Project",
            shortTitle="Test Project",
            projectSummary="Summary",
            sop="sop",
            ucrProposal="ucr_proposal",
            budgetDoc="budget_doc",
            ucrFee="no",
            ucrNoFee="yes",
            previousShortTitle="t short",
            dateAdded=datetime(2016, 2, 2),
            finalRecruitmentReport="report",
            ongoingContact=True,
            activityStartDate=datetime(2016, 2, 2),
            activityEndDate=datetime(2016, 2, 2))

        staff = models.Staff(
            userID=1,
            firstName="Aaron",
            lastName="Thomas",
            middleName="Pulver",
            email="aaron.pulver@utah.edu",
            phoneNumber="phone",
            phoneComment="phoneComment",
            institution="institution",
            department="department",
            position="position",
            credentials="credentials",
            street="street",
            city="city",
            stateID=1,
            ucrRoleID=1
        )

        ctc1 = models.CTC(
            participantID=1,
            dxDateDay=2,
            dxDateMonth=7,
            dxDateYear=1988,
            site="Site 2",
            histology="histology",
            behavior="behavior",
            ctcSequence="sequence",
            stage="stage",
            dxAge=1,
            dxStreet1="street1",
            dxStreet2="street2",
            dxCity="city",
            dxStateID=1,
            dxZip="99999",
            dxCounty="county",
            dnc="dnc",
            dncReason="dnc_reason",
            recordID="abc321"
        )

        projectPatient = models.ProjectPatient(
            projectID=1,
            staffID=1,
            ctcID=1,
            currentAge=1,
            batch=1,
            siteGrp=1,
            finalCodeID=1,
            finalCodeDate=datetime(2016, 2, 2),
            enrollmentDate=datetime(2016, 2, 2),
            dateCoordSigned=datetime(2016, 2, 2),
            importDate=datetime(2016, 2, 2),
            finalCodeStaffID=1,
            enrollmentStaffID=1,
            dateCoordSignedStaffID=1,
            abstractStatusID=1,
            abstractStatusDate=datetime(2016, 2, 2),
            abstractStatusStaffID=1,
            sentToAbstractorDate=datetime(2016, 2, 2),
            sentToAbstractorStaffID=1,
            abstractedDate=datetime(2016, 2, 2),
            abstractorStaffID=1,
            researcherDate=datetime(2016, 2, 2),
            researcherStaffID=1,
            consentLink="link",
            medRecordReleaseSigned=True,
            medRecordReleaseLink="link",
            medRecordReleaseStaffID=1,
            medRecordReleaseDate=datetime(2016, 2, 2),
            surveyToResearcher=datetime(2016, 2, 2),
            surveyToResearcherStaffID=1,
            qualityControl=True,
        )
        db.session.add_all(self.create_contact_types())
        db.session.add_all(self.create_sexes())
        db.session.add_all(self.create_races())
        db.session.add_all(self.create_ethnicities())
        db.session.add_all(self.create_vital_statuses())
        db.session.add_all(self.create_ucr_roles())
        db.session.add_all(self.create_physician_statuses())
        db.session.add_all(self.create_final_codes())
        db.session.add_all(self.create_states())
        db.session.add_all(self.create_roles())
        db.session.add_all(self.create_users())
        db.session.add_all(self.create_irb_holders())
        db.session.add_all(self.create_project_types())
        db.session.add_all(self.create_abstract_statuses())
        db.session.add_all(self.create_contact_sources())
        db.session.add_all(self.create_contact_statuses())
        db.session.add_all(self.create_phone_types())
        db.session.add(facility1)
        db.session.add(patient)
        db.session.add(informant)
        db.session.add(physician)
        db.session.add(staff)
        db.session.add(project1)
        db.session.add(ctc1)
        db.session.add(projectPatient)
        db.session.add(facility1)
        db.session.add(facilityPhone)
        db.session.add(physicianPhone)
        db.session.add(patientPhone)
        db.session.add(informantPhone)
        db.session.commit()

    def test_empty_contact(self):
        response = self.client.get("/api/contacts/")
        self.assertEqual(response.json, {"Contacts" : [] })
        
    def test_contact_no_id(self):
        response = self.client.get('/api/contacts/1/')
        self.assertEqual(response.json, {"Error" : "ContactID 1 not found"})
        
    def test_create_contact(self):
        response = self.client.post("/api/contacts/", data = {
            "contactTypeLUTID" : 1,
            "participantID" : 1,
            "staffID" : 1,
            "informantID" : 1,
            "informantPhoneID" : 1,
            "facilityID" : 1,
            "facilityPhoneID" : 1,
            "physicianID" : 1,
            "physicianPhoneID" : 1,
            "patientPhoneID" : 1,
            "description" : "desc",
            "contactDate" : "2016-02-02",
            "initials" : "atp",
            "notes" : "notes",
            "versionID" : 1,
        })
        self.assertEqual(response.json["contactTypeLUTID"], 1)
        self.assertEqual(response.json["participantID"], 1)
        self.assertEqual(response.json["staffID"], 1)
        self.assertEqual(response.json["informantID"], 1)
        self.assertEqual(response.json["informantPhoneID"], 1)
        self.assertEqual(response.json["facilityID"], 1)
        self.assertEqual(response.json["facilityPhoneID"], 1)
        self.assertEqual(response.json["physicianID"], 1)
        self.assertEqual(response.json["physicianPhoneID"], 1)
        self.assertEqual(response.json["patientPhoneID"], 1)
        self.assertEqual(response.json["description"], "desc")
        self.assertEqual(response.json["contactDate"], "2016-02-02")
        self.assertEqual(response.json["initials"], "atp")
        self.assertEqual(response.json["notes"], "notes")
        self.assertEqual(response.json["versionID"], 1)

class TestContactType(BlankDB):
    def test_empty_contact_type(self):
        response = self.client.get("/api/contacttypes/")
        self.assertEqual(response.json, {"ContactTypes" : [] })
        
    def test_contact_type_no_id(self):
        response = self.client.get('/api/contacttypes/1/')
        self.assertEqual(response.json, {"Error" : "ContactTypeID 1 not found"})
        
    def test_create_contact_type(self):
        response = self.client.post("/api/contacttypes/", data = {
            "contactDefinition" : "contactDefinition",
            "contactCode" : 100,
            "versionID" : 1,
        })
        self.assertEqual(response.json["contactDefinition"], "contactDefinition")
        self.assertEqual(response.json["contactCode"], 100)
        self.assertEqual(response.json["versionID"], 1)

class TestContactInfoStatus(BlankDB):
    def test_empty_contact_info_status(self):
        response = self.client.get("/api/contactinfostatuses/")
        self.assertEqual(response.json, {"ContactInfoStatuses" : [] })
        
    def test_contact_info_status_no_id(self):
        response = self.client.get('/api/contactinfostatuses/1/')
        self.assertEqual(response.json, {"Error" : "ContactInfoStatusID 1 not found"})
        
    def test_create_contact_info_status(self):
        response = self.client.post("/api/contactinfostatuses/", data = {
            "contactInfoStatus" : "status",
            "versionID" : 1,
        })
        self.assertEqual(response.json["contactInfoStatus"], "status")
        self.assertEqual(response.json["versionID"], 1)

class TestContactInfoSource(BlankDB):
    def test_empty_contact_info_source(self):
        response = self.client.get("/api/contactinfosources/")
        self.assertEqual(response.json, {"ContactInfoSources" : [] })
        
    def test_contact_info_source_no_id(self):
        response = self.client.get('/api/contactinfosources/1/')
        self.assertEqual(response.json, {"Error" : "ContactInfoSourceID 1 not found"})
        
    def test_create_contact_info_source(self):
        response = self.client.post("/api/contactinfosources/", data = {
            "contactInfoSource" : "source",
            "versionID" : 1,
        })
        self.assertEqual(response.json["contactInfoSource"], "source")
        self.assertEqual(response.json["versionID"], 1)

class TestCTC(BlankDB):
    def setUp(self):
        db.drop_all()
        db.create_all()
        self.populate_db()

    def populate_db(self):
        patient = models.Patient(
            patID="1",
            ucrDistID=1,
            UPDBID=1,
            firstName="fname2",
            lastName="lname2",
            middleName="mname2",
            maidenName="maiden_name",
            aliasFirstName="alias_fname",
            aliasLastName="alias_lname",
            aliasMiddleName="alias_middle",
            dobDay=26,
            dobMonth=4,
            dobYear=1970,
            SSN="999999999",
            sexID=1,
            raceID=2,
            ethnicityID=1,
            vitalStatusID=2
        )
        db.session.add_all(self.create_sexes())
        db.session.add_all(self.create_races())
        db.session.add_all(self.create_ethnicities())
        db.session.add_all(self.create_vital_statuses())
        db.session.add_all(self.create_states())

        db.session.add(patient)
        db.session.commit()

    def test_empty_ctc(self):
        response = self.client.get("/api/ctcs/")
        self.assertEqual(response.json, {"CTCs" : [] })
        
    def test_ctc_no_id(self):
        response = self.client.get('/api/ctcs/1/')
        self.assertEqual(response.json, {"Error" : "CtcID 1 not found"})
        
    def test_create_ctc(self):
        response = self.client.post("/api/ctcs/", data = {
            "participantID" : 1,
            "dxDateDay" : 1,
            "dxDateMonth" : 1,
            "dxDateYear" : 1991,
            "site" : "site",
            "histology" : "histology",
            "behavior" : "behavior",
            "ctcSequence" : "sequence",
            "stage" : "stage",
            "dxAge" : 1,
            "dxStreet1" : "street",
            "dxStreet2" : "street2",
            "dxCity" : "city",
            "dxStateID" : 1,
            "dxZip" : 99999,
            "dxCounty" : "county",
            "dnc" : "dnc",
            "dncReason" : "dnc_reason",
            "recordID": "1",
            "versionID" : 1,
        })
        self.assertEqual(response.json["participantID"], 1)
        self.assertEqual(response.json["dxDateDay"], 1)
        self.assertEqual(response.json["dxDateMonth"], 1)
        self.assertEqual(response.json["dxDateYear"], 1991)
        self.assertEqual(response.json["site"], "site")
        self.assertEqual(response.json["histology"], "histology")
        self.assertEqual(response.json["behavior"], "behavior")
        self.assertEqual(response.json["ctcSequence"], "sequence")
        self.assertEqual(response.json["stage"], "stage")
        self.assertEqual(response.json["dxAge"], 1)
        self.assertEqual(response.json["dxStreet1"], "street")
        self.assertEqual(response.json["dxStreet2"], "street2")
        self.assertEqual(response.json["dxCity"], "city")
        self.assertEqual(response.json["dxStateID"], 1)
        self.assertEqual(response.json["dxZip"], "99999")
        self.assertEqual(response.json["dxCounty"], "county")
        self.assertEqual(response.json["dnc"], "dnc")
        self.assertEqual(response.json["dncReason"], "dnc_reason")
        self.assertEqual(response.json["recordID"], "1")
        self.assertEqual(response.json["versionID"], 1)

class TestCTCFacility(BlankDB):
    def setUp(self):
        db.drop_all()
        db.create_all()
        self.populate_db()

    def populate_db(self):
        facility1 = models.Facility(
            facilityName = "name",
            contactFirstName = "fname",
            contactLastName = "lname",
            facilityStatus = 1,
            facilityStatusDate = datetime(2016,2,2),
            contact2FirstName = "fname",
            contact2LastName = "lname"
        )

        ctc1 = models.CTC(
            participantID=1,
            dxDateDay=2,
            dxDateMonth=7,
            dxDateYear=1988,
            site="Site 2",
            histology="histology",
            behavior="behavior",
            ctcSequence="sequence",
            stage="stage",
            dxAge=1,
            dxStreet1="street1",
            dxStreet2="street2",
            dxCity="city",
            dxStateID=1,
            dxZip="99999",
            dxCounty="county",
            dnc="dnc",
            dncReason="dnc_reason",
            recordID="abc321"
        )

        patient = models.Patient(
            patID="1",
            ucrDistID=1,
            UPDBID=1,
            firstName="fname2",
            lastName="lname2",
            middleName="mname2",
            maidenName="maiden_name",
            aliasFirstName="alias_fname",
            aliasLastName="alias_lname",
            aliasMiddleName="alias_middle",
            dobDay=26,
            dobMonth=4,
            dobYear=1970,
            SSN="999999999",
            sexID=1,
            raceID=2,
            ethnicityID=1,
            vitalStatusID=2
        )
        db.session.add_all(self.create_sexes())
        db.session.add_all(self.create_races())
        db.session.add_all(self.create_ethnicities())
        db.session.add_all(self.create_vital_statuses())
        db.session.add_all(self.create_states())
        db.session.add(facility1)
        db.session.add(patient)
        db.session.add(ctc1)
        db.session.commit()

    def test_empty_ctc_facility(self):
        response = self.client.get("/api/ctcfacilities/")
        self.assertEqual(response.json, dict(CTCFacilities = []))
   
    def test_ctc_facility_no_id(self):
        response = self.client.get("/api/ctcfacilities/1/")
        self.assertEqual(response.json, {"Error" : "CTCFacilityID 1 not found"})

    def test_create_ctc_facility(self):
        response = self.client.post("/api/ctcfacilities/", data = {
            "ctcID" : 1,
            "facilityID" : 1,
            "coc": 1,
            "versionID" : 1,
        })
        self.assertEqual(response.json["ctcID"], 1)
        self.assertEqual(response.json["facilityID"], 1)
        self.assertEqual(response.json["coc"], 1)
        self.assertEqual(response.json["versionID"], 1)

class TestFacilityPhone(BlankDB):
    def setUp(self):
        db.drop_all()
        db.create_all()
        self.populate_db()

    def populate_db(self):
        facility1 = models.Facility(
            facilityName = "name",
            contactFirstName = "fname",
            contactLastName = "lname",
            facilityStatus = 1,
            facilityStatusDate = datetime(2016,2,2),
            contact2FirstName = "fname",
            contact2LastName = "lname"
        )

        db.session.add_all(self.create_contact_sources())
        db.session.add_all(self.create_contact_statuses())
        db.session.add_all(self.create_phone_types())
        db.session.add(facility1)
        db.session.commit()

    def test_empty_facility_phone(self):
        response = self.client.get("/api/facilityphones/")
        self.assertEqual(response.json, dict(FacilityPhones = []))
   
    def test_facility_phone_no_id(self):
        response = self.client.get("/api/facilityphones/1/")
        self.assertEqual(response.json, {"Error" : "FacilityPhoneID 1 not found"})

    def test_create_facility_phone(self):
        response = self.client.post("/api/facilityphones/", data = {
            "contactInfoSourceID" : 1,
            "facilityID" : 1,
            "contactInfoStatusID" : 1,
            "clinicName" : "clinic",
            "phoneTypeID" : 1,
            "phoneNumber" : "phone",
            "phoneStatusDate" : "2016-02-02",
            "versionID" : 1,
        })
        self.assertEqual(response.json["facilityPhoneID"],1)
        self.assertEqual(response.json["contactInfoSourceID"],1)
        self.assertEqual(response.json["contactInfoStatusID"],1)
        self.assertEqual(response.json["clinicName"],"clinic")
        self.assertEqual(response.json["phoneTypeID"],1)
        self.assertEqual(response.json["phoneNumber"],"phone")
        self.assertEqual(response.json["phoneStatusDate"],"2016-02-02")
        self.assertEqual(response.json["versionID"],1)

class TestFacility(BlankDB):
    def test_empty_facility_phone(self):
        response = self.client.get("/api/facilities/")
        self.assertEqual(response.json, dict(Facilities = []))
   
    def test_facility_phone_no_id(self):
        response = self.client.get("/api/facilities/1/")
        self.assertEqual(response.json, {"Error" : "FacilityID 1 not found"})

    def test_create_facility_phone(self):
        response = self.client.post("/api/facilities/", data = {
            "facilityName" : "name",
            "contactFirstName" : "fname",
            "contactLastName" : "lname",
            "facilityStatus" : 1,
            "facilityStatusDate" : "2016-02-02",
            "contact2FirstName" : "fname",
            "contact2LastName" : "lname",
            "versionID" : 1,
        })
        self.assertEqual(response.json["facilityID"], 1)
        self.assertEqual(response.json["facilityName"], "name")
        self.assertEqual(response.json["contactFirstName"], "fname")
        self.assertEqual(response.json["contactLastName"], "lname")
        self.assertEqual(response.json["facilityStatus"], 1)
        self.assertEqual(response.json["facilityStatusDate"], "2016-02-02")
        self.assertEqual(response.json["contact2FirstName"], "fname")
        self.assertEqual(response.json["contact2LastName"], "lname")
        self.assertEqual(response.json["versionID"], 1)

class TestFacilityAddress(BlankDB):
    def setUp(self):
        db.drop_all()
        db.create_all()
        self.populate_db()

    def populate_db(self):
        facility1 = models.Facility(
            facilityName="name",
            contactFirstName="fname",
            contactLastName="lname",
            facilityStatus=1,
            facilityStatusDate=datetime(2016, 2, 2),
            contact2FirstName="fname",
            contact2LastName="lname"
        )

        db.session.add_all(self.create_contact_sources())
        db.session.add_all(self.create_contact_statuses())
        db.session.add_all(self.create_states())
        db.session.add(facility1)
        db.session.commit()

    def test_empty_facility_address(self):
        response = self.client.get("/api/facilityaddresses/")
        self.assertEqual(response.json, dict(FacilityAddresses = []))
   
    def test_facility_address_no_id(self):
        response = self.client.get("/api/facilityaddresses/1/")
        self.assertEqual(response.json, {"Error" : "FacilityAddressID 1 not found"})

    def test_create_facility_address(self):
        response = self.client.post("/api/facilityaddresses/", data = {
            "contactInfoSourceID" : 1,
            "facilityID" : 1,
            "contactInfoStatusID" : 1,
            "street" : "street",
            "street2" : "street2",
            "city" : "city",
            "stateID" : 1,
            "zip" : "zip",
            "addressStatusDate" : "2016-02-02",
            "versionID" : 1,
        })
        self.assertEqual(response.json["facilityAddressID"],1)
        self.assertEqual(response.json["contactInfoSourceID"],1)
        self.assertEqual(response.json["facilityID"],1)
        self.assertEqual(response.json["contactInfoStatusID"],1)
        self.assertEqual(response.json["street"],"street")
        self.assertEqual(response.json["street2"],"street2")
        self.assertEqual(response.json["city"],"city")
        self.assertEqual(response.json["stateID"],1)
        self.assertEqual(response.json["zip"],"zip")
        self.assertEqual(response.json["addressStatusDate"],"2016-02-02")
        self.assertEqual(response.json["versionID"],1)

class TestFinalCode(BlankDB):

    def test_empty_final_code(self):
        response = self.client.get("/api/finalcodes/")
        self.assertEqual(response.json, dict(FinalCodes=[]))

    def test_final_code_no_id(self):
        response = self.client.get("/api/finalcodes/1/")
        self.assertEqual(response.json, {"Error" : "FinalCodeID 1 not found"})

    def test_create_final_code(self):
        response = self.client.post("/api/finalcodes/", data = {
            "finalCodeDefinition": "def",
            "finalCode": 100
        })
        self.assertEqual(response.json["finalCodeID"],1)
        self.assertEqual(response.json["finalCodeDefinition"],"def")
        self.assertEqual(response.json["finalCode"],100)

class TestFunding(BlankDB):
    def setUp(self):
        db.drop_all()
        db.create_all()
        self.populate_db()

    def populate_db(self):
        p = models.Project(
            projectTypeID=1,
            irbHolderID=1,
            projectTitle="Test Project",
            shortTitle="Test Project",
            projectSummary="Summary",
            sop="sop",
            ucrProposal="ucr_proposal",
            budgetDoc="budget_doc",
            ucrFee="no",
            ucrNoFee="yes",
            previousShortTitle="t short",
            dateAdded=datetime(2016, 2, 2),
            finalRecruitmentReport="report",
            ongoingContact=True,
            activityStartDate=datetime(2016, 2, 2),
            activityEndDate=datetime(2016, 2, 2))

        db.session.add_all(self.create_irb_holders())
        db.session.add_all(self.create_project_types())
        db.session.add_all(self.create_grant_statuses())
        db.session.add_all(self.create_funding_sources())
        db.session.add(p)
        db.session.commit()

    def test_empty_funding(self):
        response = self.client.get("/api/fundings/")
        self.assertEqual(response.json, dict(Fundings = []))
   
    def test_funding_no_id(self):
        response = self.client.get("/api/fundings/1/")
        self.assertEqual(response.json, {"Error" : "FundingID 1 not found"})

    def test_create_funding(self):
        response = self.client.post("/api/fundings/", data = {
            "grantStatusID": 1,
            "projectID": 1,
            "fundingSourceID": 1,
            "primaryFundingSource" : "fs 1",
            "secondaryFundingSource": "fs 2",
            "fundingNumber": "number",
            "grantTitle" : "title",
            "dateStatus" : "2016-02-02",
            "grantPi": 1,
            "primaryChartfield" : "chartfield 1",
            "secondaryChartfield" : "chartfield 2",
            "versionID" : 1,
        })
        self.assertEqual(response.json["fundingID"],1)
        self.assertEqual(response.json["grantStatusID"],1)
        self.assertEqual(response.json["projectID"],1)
        self.assertEqual(response.json["fundingSourceID"],1)
        self.assertEqual(response.json["primaryFundingSource"],"fs 1")
        self.assertEqual(response.json["secondaryFundingSource"], "fs 2")
        self.assertEqual(response.json["fundingNumber"],"number")
        self.assertEqual(response.json["grantTitle"],"title")
        self.assertEqual(response.json["dateStatus"],"2016-02-02")
        self.assertEqual(response.json["grantPi"],1)
        self.assertEqual(response.json["primaryChartfield"],"chartfield 1")
        self.assertEqual(response.json["secondaryChartfield"],"chartfield 2")
        self.assertEqual(response.json["versionID"],1)

class TestFundingSource(BlankDB):

    def test_empty_funding_source(self):
        response = self.client.get("/api/fundingsources/")
        self.assertEqual(response.json, dict(FundingSources = []))
   
    def test_funding_source__no_id(self):
        response = self.client.get("/api/fundingsources/1/")
        self.assertEqual(response.json, {"Error" : "FundingSourceID 1 not found"})

    def test_create_funding_source(self):
        response = self.client.post("/api/fundingsources/", data = {
            "fundingSource" : "fs",
            "versionID" : 1,
        })
        self.assertEqual(response.json["fundingSourceID"], 1)
        self.assertEqual(response.json["fundingSource"], "fs")
        self.assertEqual(response.json["versionID"], 1)

class TestGrantStatus(BlankDB):

    def test_empty_grant_status(self):
        response = self.client.get("/api/grantstatuses/")
        self.assertEqual(response.json, dict(GrantStatuses = []))
   
    def test_grant_status__no_id(self):
        response = self.client.get("/api/grantstatuses/1/")
        self.assertEqual(response.json, {"Error" : "GrantStatusID 1 not found"})

    def test_create_grant_status(self):
        response = self.client.post("/api/grantstatuses/", data = {
            "grantStatus" : "status",
            "versionID" : 1,
        })
        self.assertEqual(response.json["grantStatusID"],1)
        self.assertEqual(response.json["grantStatus"], "status")
        self.assertEqual(response.json["versionID"],1)

class TestHumanSubjectTraining(BlankDB):
    def test_empty_human_subject_training(self):
        response = self.client.get("/api/humansubjecttrainings/")
        self.assertEqual(response.json, dict(HumanSubjectTrainings = []))
   
    def test_human_subject_training__no_id(self):
        response = self.client.get("/api/humansubjecttrainings/1/")
        self.assertEqual(response.json, {"Error" : "HumanSubjectTrainingID 1 not found"})

    def test_create_human_subject_training(self):
        response = self.client.post("/api/humansubjecttrainings/", data = {
            "trainingType" : "type",
            "versionID" : 1,
        })
        self.assertEqual(response.json["humanSubjectTrainingID"],1)
        self.assertEqual(response.json["trainingType"],"type")
        self.assertEqual(response.json["versionID"],1)

class TestIncentive(BlankDB):
    def setUp(self):
        db.drop_all()
        db.create_all()
        self.populate_db()

    def populate_db(self):
        patient = models.Patient(
            patID="1",
            ucrDistID=1,
            UPDBID=1,
            firstName="fname2",
            lastName="lname2",
            middleName="mname2",
            maidenName="maiden_name",
            aliasFirstName="alias_fname",
            aliasLastName="alias_lname",
            aliasMiddleName="alias_middle",
            dobDay=26,
            dobMonth=4,
            dobYear=1970,
            SSN="999999999",
            sexID=1,
            raceID=2,
            ethnicityID=1,
            vitalStatusID=2
        )

        project1 = models.Project(
            projectTypeID=1,
            irbHolderID=1,
            projectTitle="Test Project",
            shortTitle="Test Project",
            projectSummary="Summary",
            sop="sop",
            ucrProposal="ucr_proposal",
            budgetDoc="budget_doc",
            ucrFee="no",
            ucrNoFee="yes",
            previousShortTitle="t short",
            dateAdded=datetime(2016, 2, 2),
            finalRecruitmentReport="report",
            ongoingContact=True,
            activityStartDate=datetime(2016, 2, 2),
            activityEndDate=datetime(2016, 2, 2))

        staff = models.Staff(
            userID=1,
            firstName="Aaron",
            lastName="Thomas",
            middleName="Pulver",
            email="aaron.pulver@utah.edu",
            phoneNumber="phone",
            phoneComment="phoneComment",
            institution="institution",
            department="department",
            position="position",
            credentials="credentials",
            street="street",
            city="city",
            stateID=1,
            ucrRoleID=1
        )

        ctc1 = models.CTC(
            participantID=1,
            dxDateDay=2,
            dxDateMonth=7,
            dxDateYear=1988,
            site="Site 2",
            histology="histology",
            behavior="behavior",
            ctcSequence="sequence",
            stage="stage",
            dxAge=1,
            dxStreet1="street1",
            dxStreet2="street2",
            dxCity="city",
            dxStateID=1,
            dxZip="99999",
            dxCounty="county",
            dnc="dnc",
            dncReason="dnc_reason",
            recordID="abc321"
        )

        projectPatient = models.ProjectPatient(
            projectID=1,
            staffID=1,
            ctcID=1,
            currentAge=1,
            batch=1,
            siteGrp=1,
            finalCodeID=1,
            finalCodeDate=datetime(2016, 2, 2),
            enrollmentDate=datetime(2016, 2, 2),
            dateCoordSigned=datetime(2016, 2, 2),
            importDate=datetime(2016, 2, 2),
            finalCodeStaffID=1,
            enrollmentStaffID=1,
            dateCoordSignedStaffID=1,
            abstractStatusID=1,
            abstractStatusDate=datetime(2016, 2, 2),
            abstractStatusStaffID=1,
            sentToAbstractorDate=datetime(2016, 2, 2),
            sentToAbstractorStaffID=1,
            abstractedDate=datetime(2016, 2, 2),
            abstractorStaffID=1,
            researcherDate=datetime(2016, 2, 2),
            researcherStaffID=1,
            consentLink="link",
            medRecordReleaseSigned=True,
            medRecordReleaseLink="link",
            medRecordReleaseStaffID=1,
            medRecordReleaseDate=datetime(2016, 2, 2),
            surveyToResearcher=datetime(2016, 2, 2),
            surveyToResearcherStaffID=1,
            qualityControl=True,
        )
        contact = models.Contact(
            contactTypeLUTID=1,
            participantID=1,
            staffID=1,
            patientPhoneID=1,
            description="desc",
            contactDate=datetime(2016, 2, 2),
            initials="atp",
            notes="notes"
        )
        giftCard = models.GiftCard(
            description= "desc",
            barcode = "123456789",
            amount = 25
        )
        patientPhone = models.PatientPhone(
            contactInfoSourceID = 1,
            participantID = 1,
            contactInfoStatusID = 1,
            phoneTypeID = 1,
            phoneNumber = "123456789",
            phoneStatusDate = datetime(2016, 2, 2)
        )
        db.session.add_all(self.create_contact_types())
        db.session.add_all(self.create_sexes())
        db.session.add_all(self.create_races())
        db.session.add_all(self.create_ethnicities())
        db.session.add_all(self.create_vital_statuses())
        db.session.add_all(self.create_ucr_roles())
        db.session.add_all(self.create_physician_statuses())
        db.session.add_all(self.create_final_codes())
        db.session.add_all(self.create_states())
        db.session.add_all(self.create_roles())
        db.session.add_all(self.create_users())
        db.session.add_all(self.create_irb_holders())
        db.session.add_all(self.create_project_types())
        db.session.add_all(self.create_abstract_statuses())
        db.session.add_all(self.create_contact_sources())
        db.session.add_all(self.create_contact_statuses())
        db.session.add_all(self.create_phone_types())
        db.session.add(patient)
        db.session.commit()
        db.session.add(staff)
        db.session.commit()
        db.session.add(project1)
        db.session.commit()
        db.session.add(ctc1)
        db.session.commit()
        db.session.add(projectPatient)
        db.session.add(patientPhone)
        db.session.commit()
        db.session.add(contact)
        db.session.commit()
        db.session.add(giftCard)
        db.session.commit()

    def test_empty_incentive(self):
        response = self.client.get("/api/incentives/")
        self.assertEqual(response.json, dict(Incentives = []))

    def test_incentive__no_id(self):
        response = self.client.get("/api/incentives/1/")
        self.assertEqual(response.json, {"Error" : "IncentiveID 1 not found"})

    def test_create_incentive(self):
        response = self.client.post("/api/incentives/", data = {
            "participantID" : 1,
            "contactID": 1,
            "incentiveDescription": "desc",
            "barcode" : "123456789",
            "dateGiven" : "2016-02-02",
            "versionID" : 1,
        })
        self.assertEqual(response.json["incentiveID"],1)
        self.assertEqual(response.json["participantID"],1)
        self.assertEqual(response.json["contactID"],1)
        self.assertEqual(response.json["incentiveDescription"],"desc")
        self.assertEqual(response.json["barcode"],"123456789")
        self.assertEqual(response.json["dateGiven"],"2016-02-02")
        self.assertEqual(response.json["versionID"],1)

class TestInformant(BlankDB):
    def setUp(self):
        db.drop_all()
        db.create_all()
        self.populate_db()

    def populate_db(self):



        patient = models.Patient(
            patID="1",
            ucrDistID=1,
            UPDBID=1,
            firstName="fname2",
            lastName="lname2",
            middleName="mname2",
            maidenName="maiden_name",
            aliasFirstName="alias_fname",
            aliasLastName="alias_lname",
            aliasMiddleName="alias_middle",
            dobDay=26,
            dobMonth=4,
            dobYear=1970,
            SSN="999999999",
            sexID=1,
            raceID=2,
            ethnicityID=1,
            vitalStatusID=2
        )
        db.session.add_all(self.create_informant_relationships())
        db.session.add_all(self.create_states())
        db.session.add_all(self.create_contact_sources())
        db.session.add_all(self.create_contact_statuses())
        db.session.add_all(self.create_sexes())
        db.session.add_all(self.create_races())
        db.session.add_all(self.create_ethnicities())
        db.session.add_all(self.create_vital_statuses())
        db.session.add(patient)
        db.session.commit()

    def test_empty_informant(self):
        response = self.client.get("/api/informants/")
        self.assertEqual(response.json, dict(Informants = []))
   
    def test_informant_no_id(self):
        response = self.client.get("/api/informants/1/")
        self.assertEqual(response.json, {"Error" : "InformantID 1 not found"})

    def test_create_informant(self):
        response = self.client.post("/api/informants/", data = {
            "participantID" : 1,
            "firstName" : "fname",
            "lastName" : "lname",
            "middleName" : "middle_name",
            "informantPrimary" : "true",
            "informantRelationshipID" : 1,
            "notes" : "notes",
            "versionID" : 1,
        })
        self.assertEqual(response.json["informantID"],1)
        self.assertEqual(response.json["participantID"],1)
        self.assertEqual(response.json["firstName"],"fname")
        self.assertEqual(response.json["middleName"],"middle_name")
        self.assertEqual(response.json["informantPrimary"],True)
        self.assertEqual(response.json["informantRelationshipID"],1)
        self.assertEqual(response.json["notes"],"notes")
        self.assertEqual(response.json["versionID"],1)

class TestInformantAddress(BlankDB):
    def setUp(self):
        db.drop_all()
        db.create_all()
        self.populate_db()

    def populate_db(self):
        patient = models.Patient(
            patID="1",
            ucrDistID=1,
            UPDBID=1,
            firstName="fname2",
            lastName="lname2",
            middleName="mname2",
            maidenName="maiden_name",
            aliasFirstName="alias_fname",
            aliasLastName="alias_lname",
            aliasMiddleName="alias_middle",
            dobDay=26,
            dobMonth=4,
            dobYear=1970,
            SSN="999999999",
            sexID=1,
            raceID=2,
            ethnicityID=1,
            vitalStatusID=2
        )
        informant = models.Informant(
            participantID=1,
            firstName="fname",
            lastName="lname",
            middleName="middle_name",
            informantPrimary="informant_primary",
            informantRelationship="informant_relationship",
            notes="notes"
        )
        db.session.add_all(self.create_states())
        db.session.add_all(self.create_contact_sources())
        db.session.add_all(self.create_contact_statuses())
        db.session.add_all(self.create_sexes())
        db.session.add_all(self.create_races())
        db.session.add_all(self.create_ethnicities())
        db.session.add_all(self.create_vital_statuses())
        db.session.add(patient)
        db.session.add(informant)
        db.session.commit()
        
    def test_empty_informant_address(self):
        response = self.client.get("/api/informantaddresses/")
        self.assertEqual(response.json, dict(InformantAddresses = []))
   
    def test_informant_address_no_id(self):
        response = self.client.get("/api/informantaddresses/1/")
        self.assertEqual(response.json, {"Error" : "InformantAddressID 1 not found"})

    def test_create_informant_address(self):
        response = self.client.post("/api/informantaddresses/", data = {
            "contactInfoSourceID" : 1,
            "informantID" : 1,
            "contactInfoStatusID" : 1,
            "street" : "street",
            "street2" : "street2",
            "city" : "city",
            "stateID" : 1,
            "zip" : "12345",
            "addressStatusDate" : "2016-02-02",
            "versionID" : 1,
        })
        self.assertEqual(response.json["informantAddressID"],1)
        self.assertEqual(response.json["contactInfoSourceID"],1)
        self.assertEqual(response.json["contactInfoStatusID"],1)
        self.assertEqual(response.json["street"],"street")
        self.assertEqual(response.json["street2"],"street2")
        self.assertEqual(response.json["city"],"city")
        self.assertEqual(response.json["stateID"],1)
        self.assertEqual(response.json["zip"],"12345")
        self.assertEqual(response.json["addressStatusDate"],"2016-02-02")
        self.assertEqual(response.json["versionID"],1)

class TestInformantPhone(BlankDB):
    def setUp(self):
        db.drop_all()
        db.create_all()
        self.populate_db()

    def populate_db(self):
        patient = models.Patient(
            patID="1",
            ucrDistID=1,
            UPDBID=1,
            firstName="fname2",
            lastName="lname2",
            middleName="mname2",
            maidenName="maiden_name",
            aliasFirstName="alias_fname",
            aliasLastName="alias_lname",
            aliasMiddleName="alias_middle",
            dobDay=26,
            dobMonth=4,
            dobYear=1970,
            SSN="999999999",
            sexID=1,
            raceID=2,
            ethnicityID=1,
            vitalStatusID=2
        )
        informant = models.Informant(
            participantID=1,
            firstName="fname",
            lastName="lname",
            middleName="middle_name",
            informantPrimary="informant_primary",
            informantRelationship="informant_relationship",
            notes="notes"
        )
        db.session.add_all(self.create_states())
        db.session.add_all(self.create_contact_sources())
        db.session.add_all(self.create_contact_statuses())
        db.session.add_all(self.create_sexes())
        db.session.add_all(self.create_races())
        db.session.add_all(self.create_ethnicities())
        db.session.add_all(self.create_vital_statuses())
        db.session.add_all(self.create_phone_types())
        db.session.add(patient)
        db.session.add(informant)
        db.session.commit()

    def test_empty_informant_phone(self):
        response = self.client.get("/api/informantphones/")
        self.assertEqual(response.json, dict(InformantPhones = []))
   
    def test_informant_phone_no_id(self):
        response = self.client.get("/api/informantphones/1/")
        self.assertEqual(response.json, {"Error" : "InformantPhoneID 1 not found"})

    def test_create_informant_phone(self):
        response = self.client.post("/api/informantphones/", data = {
            "contactInfoSourceID" : 1,
            "informantID" : 1,
            "contactInfoStatusID" : 1,
            "phoneNumber" : "phone",
            "phoneTypeID" : 1,
            "phoneStatusDate" : "2016-02-02",
            "versionID" : 1,
        })
        self.assertEqual(response.json["informantPhoneID"],1)
        self.assertEqual(response.json["contactInfoSourceID"],1)
        self.assertEqual(response.json["contactInfoStatusID"],1)
        self.assertEqual(response.json["informantID"],1)
        self.assertEqual(response.json["phoneNumber"],"phone")
        self.assertEqual(response.json["phoneTypeID"],1)
        self.assertEqual(response.json["phoneStatusDate"],"2016-02-02")
        self.assertEqual(response.json["versionID"],1)

class TestIRBHolder(BlankDB):
    def test_empty_irb_holder(self):
        response = self.client.get("/api/irbholders/")
        self.assertEqual(response.json, {"irbHolders" : []})
    
    def test_irb_holder_no_id(self):
        response = self.client.get("/api/irbholders/1/")
        self.assertEqual(response.json, {"Error" : "IrbHolderID 1 not found"})
        
    def test_create_irb_holder(self):
        response = self.client.post("/api/irbholders/", data = {
            "holder" : "test holder",
            "holderDefinition" : "test holder def",
            "versionID" : 1,
            })
        self.assertEqual(response.json["irbHolderID"],1)
        self.assertEqual(response.json["holder"],"test holder")
        self.assertEqual(response.json["holderDefinition"],"test holder def")
        self.assertEqual(response.json["versionID"],1)

class TestLog(BlankDB):
    def setUp(self):
        db.drop_all()
        db.create_all()
        self.populate_db()

    def populate_db(self):
        staff = models.Staff(
            userID=1,
            firstName="Aaron",
            lastName="Thomas",
            middleName="Pulver",
            email="aaron.pulver@utah.edu",
            phoneNumber="phone",
            phoneComment="phoneComment",
            institution="institution",
            department="department",
            position="position",
            credentials="credentials",
            street="street",
            city="city",
            stateID=1,
            ucrRoleID=1
        )
        p = models.Project(
            projectTypeID=1,
            irbHolderID=1,
            projectTitle="Test Project",
            shortTitle="Test Project",
            projectSummary="Summary",
            sop="sop",
            ucrProposal="ucr_proposal",
            budgetDoc="budget_doc",
            ucrFee="no",
            ucrNoFee="yes",
            previousShortTitle="t short",
            dateAdded=datetime(2016, 2, 2),
            finalRecruitmentReport="report",
            ongoingContact=True,
            activityStartDate=datetime(2016, 2, 2),
            activityEndDate=datetime(2016, 2, 2))

        db.session.add_all(self.create_project_phases())
        db.session.add_all(self.create_irb_holders())
        db.session.add_all(self.create_project_types())
        db.session.add_all(self.create_log_subjects())
        db.session.add_all(self.create_ucr_roles())
        db.session.add_all(self.create_roles())
        db.session.add_all(self.create_users())
        db.session.add_all(self.create_states())
        db.session.add(p)
        db.session.add(staff)
        db.session.commit()

    def test_empty_log(self):
        response = self.client.get("/api/logs/")
        self.assertEqual(response.json, {"Logs" : []})
    
    def test_log_no_id(self):
        response = self.client.get("/api/logs/1/")
        self.assertEqual(response.json, {"Error" : "LogID 1 not found"})
        
    def test_create_log(self):
        response = self.client.post("/api/logs/", data = {
            "logSubjectID" : 1,
            "projectID" : 1,
            "staffID" : 1,
            "phaseStatusID" : 1,
            "note" : "note",
            "date" : "2016-02-02",
            "versionID" : 1,
            })
        self.assertEqual(response.json["logID"],1)
        self.assertEqual(response.json["projectID"],1)
        self.assertEqual(response.json["staffID"],1)
        self.assertEqual(response.json["phaseStatusID"],1)
        self.assertEqual(response.json["note"],"note")
        self.assertEqual(response.json["date"],"2016-02-02")
        self.assertEqual(response.json["versionID"],1)

class TestLogSubject(BlankDB):
    def test_empty_log_subject(self):
        response = self.client.get("/api/logsubjects/")
        self.assertEqual(response.json, {"LogSubjects" : []})
    
    def test_log_subject_no_id(self):
        response = self.client.get("/api/logsubjects/1/")
        self.assertEqual(response.json, {"Error" : "LogSubjectID 1 not found"})
        
    def test_create_log_subject(self):
        response = self.client.post("/api/logsubjects/", data = {
            "logSubject" : "subject",
            "versionID" : 1,
            })
        self.assertEqual(response.json["logSubjectID"],1)
        self.assertEqual(response.json["logSubject"],"subject")
        self.assertEqual(response.json["versionID"],1)

class TestPatient(BlankDB):

    def setUp(self):
        db.drop_all()
        db.create_all()
        self.populate_db()

    def populate_db(self):
        db.session.add_all(self.create_races())
        db.session.add_all(self.create_ethnicities())
        db.session.add_all(self.create_sexes())
        db.session.add_all(self.create_vital_statuses())

    def test_empty_patients(self):
        response = self.client.get("/api/patients/")
        self.assertEqual(response.json, dict(Patients = []))
   
    def test_patient_no_id(self):
        response = self.client.get("/api/patients/1/")
        self.assertEqual(response.json, {"Error" : "PatientID 1 not found"})

    def test_create_patient(self):
        response = self.client.post("/api/patients/", data = {
            "patID" : "123",
            "ucrDistID" : 1,
            "UPDBID" : 1,
            "firstName" : "fname",
            "lastName" : "lname",
            "middleName" : "mname",
            "maidenName" : "madien_name",
            "aliasFirstName" : "alias_fname",
            "aliasLastName" : "alias_lname",
            "aliasMiddleName" : "alias_middle",
            "dobDay" : 1,
            "dobMonth" : 1,
            "dobYear" : 1991,
            "SSN" : "999999999",
            "sexID" : 1,
            "raceID" : 1,
            "ethnicityID" : 1,
            "vitalStatusID" : 1,
            "versionID" : 1,
        })
        self.assertEqual(response.json["participantID"], 1)
        self.assertEqual(response.json["patID"], "123")
        self.assertEqual(response.json["ucrDistID"], 1)
        self.assertEqual(response.json["UPDBID"], 1)
        self.assertEqual(response.json["firstName"], "fname")
        self.assertEqual(response.json["lastName"], "lname")
        self.assertEqual(response.json["middleName"], "mname")
        self.assertEqual(response.json["maidenName"], "madien_name")
        self.assertEqual(response.json["aliasFirstName"], "alias_fname")
        self.assertEqual(response.json["aliasLastName"], "alias_lname")
        self.assertEqual(response.json["aliasMiddleName"], "alias_middle")
        self.assertEqual(response.json["dobDay"], 1)
        self.assertEqual(response.json["dobMonth"], 1)
        self.assertEqual(response.json["SSN"], "999999999")
        self.assertEqual(response.json["sexID"], 1)
        self.assertEqual(response.json["raceID"], 1)
        self.assertEqual(response.json["ethnicityID"], 1)
        self.assertEqual(response.json["vitalStatusID"], 1)
        self.assertEqual(response.json["versionID"], 1)

class TestPatientAddress(BlankDB):
    def setUp(self):
        db.drop_all()
        db.create_all()
        self.populate_db()

    def populate_db(self):
        patient = models.Patient(
            patID="1",
            ucrDistID=1,
            UPDBID=1,
            firstName="fname",
            lastName="lname",
            middleName="mname",
            maidenName="maiden_name",
            aliasFirstName="alias_fname",
            aliasLastName="alias_lname",
            aliasMiddleName="alias_middle",
            dobDay=15,
            dobMonth=2,
            dobYear=1990,
            SSN="999999999",
            sexID=2,
            raceID=1,
            ethnicityID=1,
            vitalStatusID=1
        )
        db.session.add_all(self.create_sexes())
        db.session.add_all(self.create_ethnicities())
        db.session.add_all(self.create_vital_statuses())
        db.session.add_all(self.create_races())
        db.session.add_all(self.create_states())
        db.session.add_all(self.create_contact_sources())
        db.session.add_all(self.create_contact_statuses())
        db.session.add(patient)
        db.session.commit()

    def test_empty_patient_address(self):
        response = self.client.get("/api/patientaddresses/")
        self.assertEqual(response.json, dict(PatientAddresses = []))
   
    def test_patient_address_no_id(self):
        response = self.client.get("/api/patientaddresses/1/")
        self.assertEqual(response.json, {"Error" : "PatAddressID 1 not found"})

    def test_create_patient_address(self):
        response = self.client.post("/api/patientaddresses/", data = {
            "contactInfoSourceID" : 1,
            "participantID" : 1,
            "contactInfoStatusID" : 1,
            "street" : "street",
            "street2" : "street2",
            "city" : "city",
            "stateID" : 1,
            "zip" : "zip",
            "addressStatusDate" : "2016-02-02",
            "versionID" : 1,
        })
        self.assertEqual(response.json["patAddressID"],1)
        self.assertEqual(response.json["contactInfoSourceID"],1)
        self.assertEqual(response.json["contactInfoStatusID"],1)
        self.assertEqual(response.json["street"],"street")
        self.assertEqual(response.json["street2"],"street2")
        self.assertEqual(response.json["city"],"city")
        self.assertEqual(response.json["stateID"],1)
        self.assertEqual(response.json["zip"],"zip")
        self.assertEqual(response.json["addressStatusDate"],"2016-02-02")
        self.assertEqual(response.json["versionID"],1)

class TestPatientEmail(BlankDB):
    def setUp(self):
        db.drop_all()
        db.create_all()
        self.populate_db()

    def populate_db(self):
        patient = models.Patient(
            patID="1",
            ucrDistID=1,
            UPDBID=1,
            firstName="fname",
            lastName="lname",
            middleName="mname",
            maidenName="maiden_name",
            aliasFirstName="alias_fname",
            aliasLastName="alias_lname",
            aliasMiddleName="alias_middle",
            dobDay=15,
            dobMonth=2,
            dobYear=1990,
            SSN="999999999",
            sexID=2,
            raceID=1,
            ethnicityID=1,
            vitalStatusID=1
        )
        db.session.add_all(self.create_sexes())
        db.session.add_all(self.create_ethnicities())
        db.session.add_all(self.create_vital_statuses())
        db.session.add_all(self.create_races())
        db.session.add_all(self.create_contact_sources())
        db.session.add_all(self.create_contact_statuses())
        db.session.add(patient)
        db.session.commit()

    def test_empty_patient_email(self):
        response = self.client.get("/api/patientemails/")
        self.assertEqual(response.json, dict(PatientEmails = []))
   
    def test_patient_email_no_id(self):
        response = self.client.get("/api/patientemails/1/")
        self.assertEqual(response.json, {"Error" : "EmailID 1 not found"})

    def test_create_patient_email(self):
        response = self.client.post("/api/patientemails/", data = {
            "contactInfoSourceID" : 1,
            "participantID" : 1,
            "contactInfoStatusID" : 1,
            "email" : "email",
            "emailStatusDate" : "2016-02-02",
            "versionID" : 1,
        })
        self.assertEqual(response.json["emailID"],1)
        self.assertEqual(response.json["participantID"],1)
        self.assertEqual(response.json["contactInfoStatusID"],1)
        self.assertEqual(response.json["email"],"email")
        self.assertEqual(response.json["emailStatusDate"],"2016-02-02")
        self.assertEqual(response.json["versionID"],1)

class TestPatientPhone(BlankDB):
    def setUp(self):
        db.create_all()
        self.populate_db()

    def populate_db(self):
        patient = models.Patient(
            patID="1",
            ucrDistID=1,
            UPDBID=1,
            firstName="fname",
            lastName="lname",
            middleName="mname",
            maidenName="maiden_name",
            aliasFirstName="alias_fname",
            aliasLastName="alias_lname",
            aliasMiddleName="alias_middle",
            dobDay=15,
            dobMonth=2,
            dobYear=1990,
            SSN="999999999",
            sexID=2,
            raceID=1,
            ethnicityID=1,
            vitalStatusID=1
        )
        db.session.add_all(self.create_sexes())
        db.session.add_all(self.create_ethnicities())
        db.session.add_all(self.create_vital_statuses())
        db.session.add_all(self.create_races())
        db.session.add_all(self.create_contact_sources())
        db.session.add_all(self.create_contact_statuses())
        db.session.add_all(self.create_phone_types())
        db.session.add(patient)
        db.session.commit()

    def test_empty_patient_phone(self):
        response = self.client.get("/api/patientphones/")
        self.assertEqual(response.json, dict(PatientPhones = []))
   
    def test_patient_phone_no_id(self):
        response = self.client.get("/api/patientphones/1/")
        self.assertEqual(response.json, {"Error" : "PatPhoneID 1 not found"})

    def test_create_phone_phone(self):
        response = self.client.post("/api/patientphones/", data = {
            "contactInfoSourceID" : 1,
            "participantID" : 1,
            "contactInfoStatusID" : 1,
            "phoneTypeID": 1,
            "phoneNumber" : "phone",
            "phoneStatusDate" : "2016-02-02",
            "versionID" : 1,
        })
        self.assertEqual(response.json["patPhoneID"], 1)
        self.assertEqual(response.json["contactInfoSourceID"], 1)
        self.assertEqual(response.json["participantID"], 1)
        self.assertEqual(response.json["contactInfoStatusID"], 1)
        self.assertEqual(response.json["phoneTypeID"], 1)
        self.assertEqual(response.json["phoneNumber"], "phone")
        self.assertEqual(response.json["phoneStatusDate"], "2016-02-02")
        self.assertEqual(response.json["versionID"], 1)

class TestPatientProjectStatus(BlankDB):
    def setUp(self):
        db.drop_all()
        db.create_all()
        self.populate_db()

    def populate_db(self):
        patient = models.Patient(
            patID="1",
            ucrDistID=1,
            UPDBID=1,
            firstName="fname2",
            lastName="lname2",
            middleName="mname2",
            maidenName="maiden_name",
            aliasFirstName="alias_fname",
            aliasLastName="alias_lname",
            aliasMiddleName="alias_middle",
            dobDay=26,
            dobMonth=4,
            dobYear=1970,
            SSN="999999999",
            sexID=1,
            raceID=2,
            ethnicityID=1,
            vitalStatusID=2
        )

        project1 = models.Project(
            projectTypeID=1,
            irbHolderID=1,
            projectTitle="Test Project",
            shortTitle="Test Project",
            projectSummary="Summary",
            sop="sop",
            ucrProposal="ucr_proposal",
            budgetDoc="budget_doc",
            ucrFee="no",
            ucrNoFee="yes",
            previousShortTitle="t short",
            dateAdded=datetime(2016, 2, 2),
            finalRecruitmentReport="report",
            ongoingContact=True,
            activityStartDate=datetime(2016, 2, 2),
            activityEndDate=datetime(2016, 2, 2))

        staff = models.Staff(
            userID=1,
            firstName="Aaron",
            lastName="Thomas",
            middleName="Pulver",
            email="aaron.pulver@utah.edu",
            phoneNumber="phone",
            phoneComment="phoneComment",
            institution="institution",
            department="department",
            position="position",
            credentials="credentials",
            street="street",
            city="city",
            stateID=1,
            ucrRoleID=1
        )

        ctc1 = models.CTC(
            participantID=1,
            dxDateDay=2,
            dxDateMonth=7,
            dxDateYear=1988,
            site="Site 2",
            histology="histology",
            behavior="behavior",
            ctcSequence="sequence",
            stage="stage",
            dxAge=1,
            dxStreet1="street1",
            dxStreet2="street2",
            dxCity="city",
            dxStateID=1,
            dxZip="99999",
            dxCounty="county",
            dnc="dnc",
            dncReason="dnc_reason",
            recordID="abc321"
        )

        projectPatient = models.ProjectPatient(
            projectID=1,
            staffID=1,
            ctcID=1,
            currentAge=1,
            batch=1,
            siteGrp=1,
            finalCodeID=1,
            finalCodeDate=datetime(2016, 2, 2),
            enrollmentDate=datetime(2016, 2, 2),
            dateCoordSigned=datetime(2016, 2, 2),
            importDate=datetime(2016, 2, 2),
            finalCodeStaffID=1,
            enrollmentStaffID=1,
            dateCoordSignedStaffID=1,
            abstractStatusID=1,
            abstractStatusDate=datetime(2016, 2, 2),
            abstractStatusStaffID=1,
            sentToAbstractorDate=datetime(2016, 2, 2),
            sentToAbstractorStaffID=1,
            abstractedDate=datetime(2016, 2, 2),
            abstractorStaffID=1,
            researcherDate=datetime(2016, 2, 2),
            researcherStaffID=1,
            consentLink="link",
            medRecordReleaseSigned=True,
            medRecordReleaseLink="link",
            medRecordReleaseStaffID=1,
            medRecordReleaseDate=datetime(2016, 2, 2),
            surveyToResearcher=datetime(2016, 2, 2),
            surveyToResearcherStaffID=1,
            qualityControl=True,
        )
        patientProjectStatus = models.PatientProjectStatusLUT(
            statusDescription = "desc"
        )
        db.session.add_all(self.create_sexes())
        db.session.add_all(self.create_races())
        db.session.add_all(self.create_ethnicities())
        db.session.add_all(self.create_vital_statuses())
        db.session.add_all(self.create_ucr_roles())
        db.session.add_all(self.create_physician_statuses())
        db.session.add_all(self.create_final_codes())
        db.session.add_all(self.create_states())
        db.session.add_all(self.create_roles())
        db.session.add_all(self.create_users())
        db.session.add_all(self.create_irb_holders())
        db.session.add_all(self.create_project_types())
        db.session.add_all(self.create_abstract_statuses())
        db.session.add_all(self.create_contact_sources())
        db.session.add_all(self.create_contact_statuses())
        db.session.add_all(self.create_phone_types())
        db.session.add(patient)
        db.session.add(staff)
        db.session.add(project1)
        db.session.add(ctc1)
        db.session.add(projectPatient)
        db.session.add(patientProjectStatus)
        db.session.commit()

    def test_empty_patient_project_status(self):
        response = self.client.get("/api/patientprojectstatuses/")
        self.assertEqual(response.json, dict(PatientProjectStatuses = []))
   
    def test_patient_project_status_no_id(self):
        response = self.client.get("/api/patientprojectstatuses/1/")
        self.assertEqual(response.json, {"Error" : "PatientProjectStatusID 1 not found"})

    def test_create_patient_project_status(self):
        response = self.client.post("/api/patientprojectstatuses/", data = {
            "patientProjectStatusTypeID" : 1,
            "participantID" : 1,
            "statusDate": "2016-02-02",
            "versionID" : 1,
        })
        self.assertEqual(response.json["patientProjectStatusID"],1)
        self.assertEqual(response.json["patientProjectStatusTypeID"],1)
        self.assertEqual(response.json["participantID"],1)
        self.assertEqual(response.json["statusDate"],"2016-02-02")
        self.assertEqual(response.json["versionID"],1)

class TestPatientProjectStatusLUT(BlankDB):
    def test_empty_patient_project_status_type(self):
        response = self.client.get("/api/patientprojectstatustypes/")
        self.assertEqual(response.json, dict(PatientProjectStatusTypes = []))
   
    def test_patient_project_status_type_no_id(self):
        response = self.client.get("/api/patientprojectstatustypes/1/")
        self.assertEqual(response.json, {"Error" : "PatientProjectStatusTypeID 1 not found"})

    def test_create_patient_project_status_type(self):
        response = self.client.post("/api/patientprojectstatustypes/", data = {
            "statusDescription" : "desc",
            "versionID" : 1,
        })
        self.assertEqual(response.json["patientProjectStatusTypeID"],1)
        self.assertEqual(response.json["statusDescription"],"desc")
        self.assertEqual(response.json["versionID"],1)

class TestPhaseStatus(BlankDB):
    def test_empty_phase_status(self):
        response = self.client.get("/api/phasestatuses/")
        self.assertEqual(response.json, dict(PhaseStatuses = []))
   
    def test_phase_status_no_id(self):
        response = self.client.get("/api/phasestatuses/1/")
        self.assertEqual(response.json, {"Error" : "LogPhaseID 1 not found"})

    def test_create_phase_status(self):
        response = self.client.post("/api/phasestatuses/", data = {
            "phaseStatus" : "status",
            "phaseDescription" : "description",
            "versionID" : 1,
        })
        self.assertEqual(response.json["logPhaseID"],1)
        self.assertEqual(response.json["phaseStatus"],"status")
        self.assertEqual(response.json["phaseDescription"],"description")
        self.assertEqual(response.json["versionID"],1)

class TestPhoneType(BlankDB):
    def test_emtpy_phone_type(self):
        response = self.client.get("/api/phonetypes/")
        self.assertEqual(response.json, {"PhoneTypes": []})

    def test_phone_type_no_id(self):
        response = self.client.get("/api/phonetypes/1/")
        self.assertEqual(response.json, {"Error" : "PhoneTypeID 1 not found"})

    def test_create_phone_type(self):
        response = self.client.post("/api/phonetypes/", data = {
            "phoneType" : "phoneType",
            "versionID" : 1,
        })
        self.assertEqual(response.json["phoneTypeID"],1)
        self.assertEqual(response.json["phoneType"],"phoneType")
        self.assertEqual(response.json["versionID"],1)

class TestPhysician(BlankDB):

    def setUp(self):
        db.drop_all()
        db.create_all()
        self.populate_db()

    def populate_db(self):
        db.session.add_all(self.create_physician_statuses())
        db.session.commit()

    def test_empty_physician(self):
        response = self.client.get("/api/physicians/")
        self.assertEqual(response.json, dict(Physicians = []))
   
    def test_physician_no_id(self):
        response = self.client.get("/api/physicians/1/")
        self.assertEqual(response.json, {"Error" : "PhysicianID 1 not found"})

    def test_create_physician(self):
        response = self.client.post("/api/physicians/", data = {
            "firstName" : "fname",
            "lastName" : "lname",
            "middleName" : "middle_name",
            "credentials" : "credentials",
            "specialty" : "specialty",
            "aliasFirstName" : "alias_fname",
            "aliasLastName" : "alias_lname",
            "aliasMiddleName" : "alias_middle_name",
            "physicianStatusID" : 1,
            "physicianStatusDate" : "2016-02-02",
            "versionID" : 1,
        })
        self.assertEqual(response.json["physicianID"],1)
        self.assertEqual(response.json["firstName"],"fname")
        self.assertEqual(response.json["lastName"],"lname")
        self.assertEqual(response.json["middleName"],"middle_name")
        self.assertEqual(response.json["credentials"],"credentials")
        self.assertEqual(response.json["specialty"],"specialty")
        self.assertEqual(response.json["aliasFirstName"],"alias_fname")
        self.assertEqual(response.json["aliasLastName"],"alias_lname")
        self.assertEqual(response.json["aliasMiddleName"],"alias_middle_name")
        self.assertEqual(response.json["physicianStatusID"],1)
        self.assertEqual(response.json["physicianStatusDate"],"2016-02-02")
        self.assertEqual(response.json["versionID"],1)

class TestPhysicianAddress(BlankDB):
    def setUp(self):
        db.drop_all()
        db.create_all()
        self.populate_db()

    def populate_db(self):
        physician = models.Physician(
            firstName = "fname",
            lastName = "lname",
            middleName = "middle_name",
            credentials = "credentials",
            specialty = "specialty",
            aliasFirstName = "alias_fname",
            aliasLastName = "alias_lname",
            aliasMiddleName = "alias_middle_name",
            physicianStatusID = 1,
            physicianStatusDate = datetime(2016,2,2),
        )
        db.session.add_all(self.create_contact_sources())
        db.session.add_all(self.create_contact_statuses())
        db.session.add_all(self.create_physician_statuses())
        db.session.add_all(self.create_states())
        db.session.add(physician)
        db.session.commit()

    def test_empty_physician_address(self):
        response = self.client.get("/api/physicianaddresses/")
        self.assertEqual(response.json, dict(PhysicianAddresses = []))
   
    def test_physician_address_no_id(self):
        response = self.client.get("/api/physicianaddresses/1/")
        self.assertEqual(response.json, {"Error" : "PhysicianAddressID 1 not found"})

    def test_create_physician_address(self):
        response = self.client.post("/api/physicianaddresses/", data = {
            "contactInfoSourceID" : 1,
            "physicianID" : 1,
            "contactInfoStatusID" : 1,
            "street" : "street",
            "street2" : "street2",
            "city" : "city",
            "stateID" : 1,
            "zip" : "zip",
            "addressStatusDate" : "2016-02-02",
            "versionID" : 1,
        })
        self.assertEqual(response.json["physicianAddressID"],1)
        self.assertEqual(response.json["physicianID"],1)
        self.assertEqual(response.json["contactInfoSourceID"],1)
        self.assertEqual(response.json["contactInfoStatusID"],1)
        self.assertEqual(response.json["street"],"street")
        self.assertEqual(response.json["street2"],"street2")
        self.assertEqual(response.json["city"],"city")
        self.assertEqual(response.json["stateID"],1)
        self.assertEqual(response.json["zip"],"zip")
        self.assertEqual(response.json["addressStatusDate"],"2016-02-02")
        self.assertEqual(response.json["versionID"],1)

class TestPhysicianEmail(BlankDB):
    def setUp(self):
        db.drop_all()
        db.create_all()
        self.populate_db()

    def populate_db(self):
        physician = models.Physician(
            firstName = "fname",
            lastName = "lname",
            middleName = "middle_name",
            credentials = "credentials",
            specialty = "specialty",
            aliasFirstName = "alias_fname",
            aliasLastName = "alias_lname",
            aliasMiddleName = "alias_middle_name",
            physicianStatusID = 1,
            physicianStatusDate = datetime(2016,2,2),
        )
        db.session.add_all(self.create_contact_sources())
        db.session.add_all(self.create_contact_statuses())
        db.session.add_all(self.create_physician_statuses())
        db.session.add(physician)
        db.session.commit()

    def test_empty_physician_email(self):
        response = self.client.get("/api/physicianemails/")
        self.assertEqual(response.json, dict(PhysicianEmails = []))

    def test_physician_email_no_id(self):
        response = self.client.get("/api/physicianemails/1/")
        self.assertEqual(response.json, {"Error" : "PhysicianEmailID 1 not found"})

    def test_create_physician_email(self):
        response = self.client.post("/api/physicianemails/", data = {
            "contactInfoSourceID" : 1,
            "physicianID" : 1,
            "contactInfoStatusID" : 1,
            "email" : "email",
            "emailStatusDate" : "2016-02-02",
            "versionID" : 1,
        })
        self.assertEqual(response.json["physicianEmailID"],1)
        self.assertEqual(response.json["contactInfoSourceID"],1)
        self.assertEqual(response.json["physicianID"],1)
        self.assertEqual(response.json["contactInfoStatusID"],1)
        self.assertEqual(response.json["email"],"email")
        self.assertEqual(response.json["emailStatusDate"],"2016-02-02")
        self.assertEqual(response.json["versionID"],1)

class TestPhysicianFacility(BlankDB):

    def setUp(self):
        db.drop_all()
        db.create_all()
        self.populate_db()

    def populate_db(self):
        facility1 = models.Facility(
            facilityName = "name",
            contactFirstName = "fname",
            contactLastName = "lname",
            facilityStatus = 1,
            facilityStatusDate = datetime(2016,2,2),
            contact2FirstName = "fname",
            contact2LastName = "lname"
        )
        physician = models.Physician(
            firstName = "fname",
            lastName = "lname",
            middleName = "middle_name",
            credentials = "credentials",
            specialty = "specialty",
            aliasFirstName = "alias_fname",
            aliasLastName = "alias_lname",
            aliasMiddleName = "alias_middle_name",
            physicianStatusID = 1,
            physicianStatusDate = datetime(2016,2,2),
        )
        db.session.add_all(self.create_physician_statuses())
        db.session.add_all(self.create_physician_facility_statuses())
        db.session.add(facility1)
        db.session.add(physician)
        db.session.commit()

    def test_empty_physician_facility(self):
        response = self.client.get("/api/physicianfacilities/")
        self.assertEqual(response.json, dict(PhysicianFacilities = []))
   
    def test_physician_facility_no_id(self):
        response = self.client.get("/api/physicianfacilities/1/")
        self.assertEqual(response.json, {"Error" : "PhysFacilityID 1 not found"})

    def test_create_physician_facility(self):
        response = self.client.post("/api/physicianfacilities/", data = {
            "facilityID" : 1,
            "physicianID" : 1,
            "physFacilityStatusID" : 1,
            "physFacilityStatusDate" : "2016-02-02",
            "versionID" : 1,
        })
        self.assertEqual(response.json["physFacilityID"],1)
        self.assertEqual(response.json["facilityID"],1)
        self.assertEqual(response.json["physicianID"],1)
        self.assertEqual(response.json["physFacilityStatusID"],1)
        self.assertEqual(response.json["physFacilityStatusDate"],"2016-02-02")
        self.assertEqual(response.json["versionID"],1)

class TestPhysicianPhone(BlankDB):
    def setUp(self):
        db.drop_all()
        db.create_all()
        self.populate_db()

    def populate_db(self):
        physician = models.Physician(
            firstName="fname",
            lastName="lname",
            middleName="middle_name",
            credentials="credentials",
            specialty="specialty",
            aliasFirstName="alias_fname",
            aliasLastName="alias_lname",
            aliasMiddleName="alias_middle_name",
            physicianStatusID=1,
            physicianStatusDate=datetime(2016, 2, 2),
        )
        db.session.add_all(self.create_contact_sources())
        db.session.add_all(self.create_contact_statuses())
        db.session.add_all(self.create_physician_statuses())
        db.session.add_all(self.create_phone_types())
        db.session.add(physician)
        db.session.commit()

    def test_empty_physician_phone(self):
        response = self.client.get("/api/physicianphones/")
        self.assertEqual(response.json, dict(PhysicianPhones = []))
   
    def test_physician_phone_no_id(self):
        response = self.client.get("/api/physicianphones/1/")
        self.assertEqual(response.json, {"Error" : "PhysicianPhoneID 1 not found"})

    def test_create_phone_phone(self):
        response = self.client.post("/api/physicianphones/", data = {
            "contactInfoSourceID" : 1,
            "physicianID" : 1,
            "contactInfoStatusID" : 1,
            "phoneNumber" : "phone",
            "phoneTypeID" : 1,
            "phoneStatusDate" : "2016-02-02",
            "versionID" : 1,
        })
        self.assertEqual(response.json["physicianPhoneID"],1)
        self.assertEqual(response.json["contactInfoSourceID"],1)
        self.assertEqual(response.json["physicianID"],1)
        self.assertEqual(response.json["contactInfoStatusID"],1)
        self.assertEqual(response.json["phoneNumber"],"phone")
        self.assertEqual(response.json["phoneTypeID"],1)
        self.assertEqual(response.json["phoneStatusDate"],"2016-02-02")
        self.assertEqual(response.json["versionID"],1)

class TestPhysicianToCTC(BlankDB):
    def setUp(self):
        db.drop_all()
        db.create_all()
        self.populate_db()

    def populate_db(self):
        patient = models.Patient(
            patID="1",
            ucrDistID=1,
            UPDBID=1,
            firstName="fname",
            lastName="lname",
            middleName="mname",
            maidenName="maiden_name",
            aliasFirstName="alias_fname",
            aliasLastName="alias_lname",
            aliasMiddleName="alias_middle",
            dobDay=15,
            dobMonth=2,
            dobYear=1990,
            SSN="999999999",
            sexID=2,
            raceID=1,
            ethnicityID=1,
            vitalStatusID=1
        )

        ctc = models.CTC(
            participantID=1,
            dxDateDay=2,
            dxDateMonth=7,
            dxDateYear=1988,
            site="Site 2",
            histology="histology",
            behavior="behavior",
            ctcSequence="sequence",
            stage="stage",
            dxAge=1,
            dxStreet1="street1",
            dxStreet2="street2",
            dxCity="city",
            dxStateID=1,
            dxZip=99999,
            dxCounty="county",
            dnc="dnc",
            dncReason="dnc_reason",
            recordID="abc321"
        )
        physician = models.Physician(
            firstName = "fname",
            lastName = "lname",
            middleName = "middle_name",
            credentials = "credentials",
            specialty = "specialty",
            aliasFirstName = "alias_fname",
            aliasLastName = "alias_lname",
            aliasMiddleName = "alias_middle_name",
            physicianStatusID = 1,
            physicianStatusDate = datetime(2016,2,2),
        )
        db.session.add_all(self.create_races())
        db.session.add_all(self.create_sexes())
        db.session.add_all(self.create_vital_statuses())
        db.session.add_all(self.create_ethnicities())
        db.session.add_all(self.create_physician_statuses())
        db.session.add_all(self.create_states())
        db.session.add(patient)
        db.session.add(physician)
        db.session.add(ctc)
        db.session.commit()

    def test_empty_physician_to_ctc(self):
        response = self.client.get("/api/physiciantoctcs/")
        self.assertEqual(response.json, dict(PhysicianToCTCs = []))
   
    def test_physician_to_ctc_no_id(self):
        response = self.client.get("/api/physiciantoctcs/1/")
        self.assertEqual(response.json, {"Error" : "PhysicianCTCID 1 not found"})

    def test_create_physician_to_ctc(self):
        response = self.client.post("/api/physiciantoctcs/", data = {
            "physicianID" : 1,
            "ctcID" : 1,
            "versionID" : 1,
        })
        self.assertEqual(response.json["physicianCTCID"],1)
        self.assertEqual(response.json["physicianID"],1)
        self.assertEqual(response.json["ctcID"],1)
        self.assertEqual(response.json["versionID"],1)

class TestPreApplication(BlankDB):
    def setUp(self):
        db.drop_all()
        db.create_all()
        self.populate_db()

    def populate_db(self):
        p = models.Project(
            projectTypeID=1,
            irbHolderID=1,
            projectTitle="Test Project",
            shortTitle="Test Project",
            projectSummary="Summary",
            sop="sop",
            ucrProposal="ucr_proposal",
            budgetDoc="budget_doc",
            ucrFee="no",
            ucrNoFee="yes",
            previousShortTitle="t short",
            dateAdded=datetime(2016, 2, 2),
            finalRecruitmentReport="report",
            ongoingContact=True,
            activityStartDate=datetime(2016, 2, 2),
            activityEndDate=datetime(2016, 2, 2))

        db.session.add_all(self.create_irb_holders())
        db.session.add_all(self.create_project_types())
        db.session.add(p)
        db.session.commit()

    def test_empty_pre_application(self):
        response = self.client.get("/api/preapplications/")
        self.assertEqual(response.json, dict(PreApplications = []))
   
    def test_pre_application_no_id(self):
        response = self.client.get("/api/preapplications/1/")
        self.assertEqual(response.json, {"Error" : "PreApplicationID 1 not found"})

    def test_create_pre_application(self):
        response = self.client.post("/api/preapplications/", data = {
            "projectID" : 1,
            "piFirstName" : "pi_fname",
            "piLastName" : "pi_lname",
            "piEmail" : "pi_email",
            "piPhone" : "pi_phone",
            "contactFirstName" : "contact_fname",
            "contactLastName" : "contact_lname",
            "contactPhone" : "contact_phone",
            "contactEmail" : "contact_email",
            "institution" : "institution",
            "institution2" : "institution2",
            "uid" : "uid",
            "udoh" : 1,
            "projectTitle" : "project_title",
            "purpose" : "purpose",
            "irb0" : "true",
            "irb1" : "true",
            "irb2" : "true",
            "irb3" : "true",
            "irb4" : "true",
            "otherIrb" : "other_irb",
            "updb" : "true",
            "ptContact" : "true",
            "startDate" : "2016-02-02",
            "link" : "true",
            "deliveryDate" : "2016-02-02",
            "description" : "description",
            "versionID" : 1,
        })
        self.assertEqual(response.json["preApplicationID"],1)
        self.assertEqual(response.json["projectID"],1)
        self.assertEqual(response.json["piFirstName"],"pi_fname")
        self.assertEqual(response.json["piLastName"],"pi_lname")
        self.assertEqual(response.json["piEmail"],"pi_email")
        self.assertEqual(response.json["piPhone"],"pi_phone")
        self.assertEqual(response.json["contactFirstName"],"contact_fname")
        self.assertEqual(response.json["contactLastName"],"contact_lname")
        self.assertEqual(response.json["contactPhone"],"contact_phone")
        self.assertEqual(response.json["contactEmail"],"contact_email")
        self.assertEqual(response.json["institution"],"institution")
        self.assertEqual(response.json["institution2"],"institution2")
        self.assertEqual(response.json["uid"],"uid")
        self.assertEqual(response.json["udoh"],1)
        self.assertEqual(response.json["projectTitle"],"project_title")
        self.assertEqual(response.json["purpose"],"purpose")
        self.assertEqual(response.json["irb0"],True)
        self.assertEqual(response.json["irb1"],True)
        self.assertEqual(response.json["irb2"],True)
        self.assertEqual(response.json["irb3"],True)
        self.assertEqual(response.json["irb4"],True)
        self.assertEqual(response.json["otherIrb"],"other_irb")
        self.assertEqual(response.json["updb"],True)
        self.assertEqual(response.json["ptContact"],True)
        self.assertEqual(response.json["startDate"],"2016-02-02")
        self.assertEqual(response.json["link"],True)
        self.assertEqual(response.json["deliveryDate"],"2016-02-02")
        self.assertEqual(response.json["description"],"description")
        self.assertEqual(response.json["versionID"],1)

class TestProject(BlankDB):
    def setUp(self):
        db.drop_all()
        db.create_all()
        self.populate_db()

    def populate_db(self):
        # Need to populate the FK tables with stuff
        db.session.add_all(self.create_irb_holders())
        db.session.add_all(self.create_project_types())
        db.session.commit()

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
    def test_create_project(self):
        response = self.client.post("/api/projects/", data = {
            "projectTypeID" : 1,
            "irbHolderID" : 1,
            "projectTitle" : "Test Project",
            "shortTitle" : "Test Project",
            "projectSummary" : "Summary",
            "sop":"sop",
            "ucrProposal":"ucr_proposal",
            "budgetDoc" : "budget_doc",
            "ucrFee" : "no",
            "ucrNoFee" : "yes",
            "previousShortTitle" : "t short",
            "dateAdded" : "2016-02-02",
            "finalRecruitmentReport" : "report",
            "ongoingContact" : "true",
            "activityStartDate" : "2016-02-02",
            "activityEndDate" : "2016-02-02",
            "versionID" : 1,})
        self.assertEqual(response.json["projectID"],1)
        self.assertEqual(response.json["projectTypeID"],1)
        self.assertEqual(response.json["irbHolderID"],1)
        self.assertEqual(response.json["projectTitle"],"Test Project")
        self.assertEqual(response.json["shortTitle"],"Test Project")
        self.assertEqual(response.json["projectSummary"],"Summary")
        self.assertEqual(response.json["sop"],"sop")
        self.assertEqual(response.json["ucrProposal"],"ucr_proposal")
        self.assertEqual(response.json["budgetDoc"],"budget_doc")
        self.assertEqual(response.json["ucrFee"],"no")
        self.assertEqual(response.json["ucrNoFee"],"yes")
        self.assertEqual(response.json["previousShortTitle"],"t short")
        self.assertEqual(response.json["dateAdded"],"2016-02-02")
        self.assertEqual(response.json["finalRecruitmentReport"],"report")
        self.assertEqual(response.json["ongoingContact"], True)
        self.assertEqual(response.json["activityStartDate"],"2016-02-02")
        self.assertEqual(response.json["activityEndDate"],"2016-02-02")
        self.assertEqual(response.json["versionID"],1)

class TestProjectPatient(BlankDB):
    def setUp(self):
        db.drop_all()
        db.create_all()
        self.populate_db()

    def populate_db(self):
        patient = models.Patient(
            patID="1",
            ucrDistID=1,
            UPDBID=1,
            firstName="fname2",
            lastName="lname2",
            middleName="mname2",
            maidenName="maiden_name",
            aliasFirstName="alias_fname",
            aliasLastName="alias_lname",
            aliasMiddleName="alias_middle",
            dobDay=26,
            dobMonth=4,
            dobYear=1970,
            SSN="999999999",
            sexID=1,
            raceID=2,
            ethnicityID=1,
            vitalStatusID=2
        )

        project1 = models.Project(
            projectTypeID=1,
            irbHolderID=1,
            projectTitle="Test Project",
            shortTitle="Test Project",
            projectSummary="Summary",
            sop="sop",
            ucrProposal="ucr_proposal",
            budgetDoc="budget_doc",
            ucrFee="no",
            ucrNoFee="yes",
            previousShortTitle="t short",
            dateAdded=datetime(2016, 2, 2),
            finalRecruitmentReport="report",
            ongoingContact=True,
            activityStartDate=datetime(2016, 2, 2),
            activityEndDate=datetime(2016, 2, 2))

        staff = models.Staff(
            userID=1,
            firstName="Aaron",
            lastName="Thomas",
            middleName="Pulver",
            email="aaron.pulver@utah.edu",
            phoneNumber="phone",
            phoneComment="phoneComment",
            institution="institution",
            department="department",
            position="position",
            credentials="credentials",
            street="street",
            city="city",
            stateID=1,
            ucrRoleID=1
        )

        ctc1 = models.CTC(
            participantID=1,
            dxDateDay=2,
            dxDateMonth=7,
            dxDateYear=1988,
            site="Site 2",
            histology="histology",
            behavior="behavior",
            ctcSequence="sequence",
            stage="stage",
            dxAge=1,
            dxStreet1="street1",
            dxStreet2="street2",
            dxCity="city",
            dxStateID=1,
            dxZip="99999",
            dxCounty="county",
            dnc="dnc",
            dncReason="dnc_reason",
            recordID="abc321"
        )
        db.session.add_all(self.create_contact_types())
        db.session.add_all(self.create_sexes())
        db.session.add_all(self.create_races())
        db.session.add_all(self.create_ethnicities())
        db.session.add_all(self.create_vital_statuses())
        db.session.add_all(self.create_ucr_roles())
        db.session.add_all(self.create_final_codes())
        db.session.add_all(self.create_states())
        db.session.add_all(self.create_roles())
        db.session.add_all(self.create_users())
        db.session.add_all(self.create_irb_holders())
        db.session.add_all(self.create_project_types())
        db.session.add_all(self.create_abstract_statuses())
        db.session.add_all(self.create_phone_types())
        db.session.add(patient)
        db.session.add(staff)
        db.session.add(project1)
        db.session.add(ctc1)
        db.session.commit()

    def test_empty_project_patient(self):
        response = self.client.get("/api/projectpatients/")
        self.assertEqual(response.json, dict(ProjectPatients = []))
   
    def test_project_patient_no_id(self):
        response = self.client.get("/api/projectpatients/1/")
        self.assertEqual(response.json, {"Error" : "ParticipantID 1 not found"})

    def test_create_project_patient(self):
        response = self.client.post("/api/projectpatients/", data = {
            "projectID" : 1,
            "staffID" : 1,
            "ctcID" : 1,
            "currentAge" : 1,
            "batch"  : 1,
            "siteGrp" : 1,
            "finalCodeID" : 1,
            "finalCodeDate" : "2016-02-02",
            "enrollmentDate" : "2016-02-02",
            "dateCoordSigned" : "2016-02-02",
            "importDate" : "2016-02-02",
            "finalCodeStaffID" : 1,
            "enrollmentStaffID" : 1,
            "dateCoordSignedStaffID"  : 1,
            "abstractStatusID" : 1,
            "abstractStatusDate" : "2016-02-02",
            "abstractStatusStaffID" : 1,
            "sentToAbstractorDate"  : "2016-02-02",
            "sentToAbstractorStaffID" : 1,
            "abstractedDate" : "2016-02-02",
            "abstractorStaffID" : 1,
            "researcherDate" : "2016-02-02",
            "researcherStaffID" : 1,
            "consentLink" : "consent",
            "medRecordReleaseSigned" : "true",
            "medRecordReleaseLink" : "link",
            "medRecordReleaseStaffID" : 1,
            "medRecordReleaseDate"  : "2016-02-02",
            "surveyToResearcher"  : "2016-02-02",
            "surveyToResearcherStaffID" : 1,
            "versionID" : 1,
        })
        self.assertEqual(response.json["participantID"],1)
        self.assertEqual(response.json["projectID"],1)
        self.assertEqual(response.json["staffID"],1)
        self.assertEqual(response.json["ctcID"],1)
        self.assertEqual(response.json["currentAge"],1)
        self.assertEqual(response.json["batch"],1)
        self.assertEqual(response.json["siteGrp"],1)
        self.assertEqual(response.json["finalCodeID"],1)
        self.assertEqual(response.json["finalCodeDate"],"2016-02-02")
        self.assertEqual(response.json["enrollmentDate"],"2016-02-02")
        self.assertEqual(response.json["importDate"],"2016-02-02")
        self.assertEqual(response.json["finalCodeStaffID"],1)
        self.assertEqual(response.json["enrollmentStaffID"],1)
        self.assertEqual(response.json["dateCoordSignedStaffID"],1)
        self.assertEqual(response.json["abstractStatusID"],1)
        self.assertEqual(response.json["abstractStatusDate"],"2016-02-02")
        self.assertEqual(response.json["abstractStatusStaffID"],1)
        self.assertEqual(response.json["sentToAbstractorDate"],"2016-02-02")
        self.assertEqual(response.json["sentToAbstractorStaffID"],1)
        self.assertEqual(response.json["researcherDate"],"2016-02-02")
        self.assertEqual(response.json["researcherStaffID"],1)
        self.assertEqual(response.json["consentLink"],"consent")
        self.assertEqual(response.json["medRecordReleaseSigned"],True)
        self.assertEqual(response.json["medRecordReleaseLink"],"link")
        self.assertEqual(response.json["medRecordReleaseStaffID"],1)
        self.assertEqual(response.json["medRecordReleaseDate"],"2016-02-02")
        self.assertEqual(response.json["surveyToResearcher"],"2016-02-02")
        self.assertEqual(response.json["surveyToResearcherStaffID"],1)
        self.assertEqual(response.json["versionID"],1)

class TestProjectStaff(BlankDB):
    def setUp(self):
        db.drop_all()
        db.create_all()
        self.populate_db()

    def populate_db(self):
        p = models.Project(
            projectTypeID=1,
            irbHolderID=1,
            projectTitle="Test Project",
            shortTitle="Test Project",
            projectSummary="Summary",
            sop="sop",
            ucrProposal="ucr_proposal",
            budgetDoc="budget_doc",
            ucrFee="no",
            ucrNoFee="yes",
            previousShortTitle="t short",
            dateAdded=datetime(2016, 2, 2),
            finalRecruitmentReport="report",
            ongoingContact=True,
            activityStartDate=datetime(2016, 2, 2),
            activityEndDate=datetime(2016, 2, 2))

        staff = models.Staff(
            userID=1,
            firstName="Aaron",
            lastName="Thomas",
            middleName="Pulver",
            email="aaron.pulver@utah.edu",
            phoneNumber="phone",
            phoneComment="phoneComment",
            institution="institution",
            department="department",
            position="position",
            credentials="credentials",
            street="street",
            city="city",
            stateID=1,
            ucrRoleID=1
        )

        db.session.add_all(self.create_irb_holders())
        db.session.add_all(self.create_project_types())
        db.session.add_all(self.create_staff_roles())
        db.session.add_all(self.create_states())
        db.session.add_all(self.create_roles())
        db.session.add_all(self.create_users())
        db.session.add_all(self.create_inactives())
        db.session.add_all(self.create_contacts())
        db.session.add_all(self.create_ucr_roles())
        db.session.add(staff)
        db.session.add(p)
        db.session.commit()

    def test_empty_project_staff(self):
        response = self.client.get("/api/projectstaff/")
        self.assertEqual(response.json, {"ProjectStaff" : []})
    
    def test_project_staff_no_id(self):
        response = self.client.get("/api/projectstaff/1/")
        self.assertEqual(response.json, {"Error" : "ProjectStaffID 1 not found"})
        
    def test_create_project_staff(self):
        response = self.client.post("/api/projectstaff/", data = {
            "staffRoleID" : 1,
            "projectID" : 1,
            "staffID" : 1,
            "datePledge" : "2016-02-02",
            "dateRevoked" : "2016-02-02",
            "contactID" : 1,
            "inactiveID" : 1,
            "versionID" : 1,
            })
        self.assertEqual(response.json["projectStaffID"],1)
        self.assertEqual(response.json["staffRoleID"],1)
        self.assertEqual(response.json["projectID"],1)
        self.assertEqual(response.json["staffID"],1)
        self.assertEqual(response.json["datePledge"],"2016-02-02")
        self.assertEqual(response.json["dateRevoked"],"2016-02-02")
        self.assertEqual(response.json["contactID"],1)
        self.assertEqual(response.json["inactiveID"],1)
        self.assertEqual(response.json["versionID"],1)

class TestProjectStatus(BlankDB):
    def setUp(self):
        db.drop_all()
        db.create_all()
        self.populate_db()

    def populate_db(self):
        p = models.Project(
            projectTypeID=1,
            irbHolderID=1,
            projectTitle="Test Project",
            shortTitle="Test Project",
            projectSummary="Summary",
            sop="sop",
            ucrProposal="ucr_proposal",
            budgetDoc="budget_doc",
            ucrFee="no",
            ucrNoFee="yes",
            previousShortTitle="t short",
            dateAdded=datetime(2016, 2, 2),
            finalRecruitmentReport="report",
            ongoingContact=True,
            activityStartDate=datetime(2016, 2, 2),
            activityEndDate=datetime(2016, 2, 2))

        staff = models.Staff(
            userID=1,
            firstName="Aaron",
            lastName="Thomas",
            middleName="Pulver",
            email="aaron.pulver@utah.edu",
            phoneNumber="phone",
            phoneComment="phoneComment",
            institution="institution",
            department="department",
            position="position",
            credentials="credentials",
            street="street",
            city="city",
            stateID=1,
            ucrRoleID=1
        )
        projStatusType = models.ProjectStatusLUT(
            projectStatus = "Status 1",
            projectStatusDefinition = "status def"
        )

        db.session.add_all(self.create_irb_holders())
        db.session.add_all(self.create_project_types())
        db.session.add_all(self.create_staff_roles())
        db.session.add_all(self.create_states())
        db.session.add_all(self.create_roles())
        db.session.add_all(self.create_users())
        db.session.add_all(self.create_ucr_roles())
        db.session.add(staff)
        db.session.add(projStatusType)
        db.session.add(p)
        db.session.commit()

    def test_empty_project_status(self):
        response = self.client.get("/api/projectstatuses/")
        self.assertEqual(response.json, dict(ProjectStatuses = []))
   
    def test_project_status_no_id(self):
        response = self.client.get("/api/projectstatuses/1/")
        self.assertEqual(response.json, {"Error" : "ProjectStatusID 1 not found"})

    def test_create_project_status(self):
        response = self.client.post("/api/projectstatuses/", data = {
            "projectStatusTypeID" : 1,
            "projectID" : 1,
            "staffID" : 1,
            "statusDate" : "2016-02-02",
            "statusNotes" : "note",
            "versionID" : 1,
        })
        self.assertEqual(response.json["projectStatusID"],1)
        self.assertEqual(response.json["projectID"],1)
        self.assertEqual(response.json["staffID"],1)
        self.assertEqual(response.json["statusDate"],"2016-02-02")
        self.assertEqual(response.json["statusNotes"],"note")
        self.assertEqual(response.json["versionID"],1)

class TestProjectStatusType(BlankDB):

    def test_empty_project_status_type(self):
        response = self.client.get("/api/projectstatustypes/")
        self.assertEqual(response.json, dict(ProjectStatusTypes = []))
   
    def test_project_status_type_no_id(self):
        response = self.client.get("/api/projectstatustypes/1/")
        self.assertEqual(response.json, {"Error" : "ProjectStatusTypeID 1 not found"})

    def test_create_project_status_type(self):
        response = self.client.post("/api/projectstatustypes/", data = {
            "projectStatus" : "Status 1",
            "projectStatusDefinition" : "status def",
            "versionID" : 1,
        })
        self.assertEqual(response.json["projectStatusTypeID"],1)
        self.assertEqual(response.json["projectStatus"],"Status 1")
        self.assertEqual(response.json["projectStatusDefinition"],"status def")
        self.assertEqual(response.json["versionID"],1)

class TestProjectType(BlankDB):

    def test_empty_project_type(self):
        response = self.client.get("/api/projecttypes/")
        self.assertEqual(response.json, dict(ProjectTypes = []))
   
    def test_project_status__no_id(self):
        response = self.client.get("/api/projecttypes/1/")
        self.assertEqual(response.json, {"Error" : "ProjectTypeID 1 not found"})

    def test_create_project_type(self):
        response = self.client.post("/api/projecttypes/", data = {
            "projectType" : "type",
            "projectTypeDefinition" : "type def",
            "versionID" : 1,
        })
        self.assertEqual(response.json["projectTypeID"],1)
        self.assertEqual(response.json["projectType"],"type")
        self.assertEqual(response.json["projectTypeDefinition"],"type def")
        self.assertEqual(response.json["versionID"],1)

class ReviewCommitteeStatusLUT(BlankDB):
    # Test for empty RCStatusList
    def test_empty_rcStatusList(self):
        response = self.client.get("/api/reviewcommitteestatuses/")
        self.assertEqual(response.json, dict(ReviewCommitteeStatuses = []))
    # Test for rcStatusList not found    
    def test_rcStatusList_no_id(self):
        response = self.client.get("/api/reviewcommitteestatuses/1/")
        self.assertEqual(response.json, {"Error" : "ReviewCommitteeStatusID 1 not found"})
    # Test create RCStatusList
    def test_create_rcStatusList(self):
        response = self.client.post("/api/reviewcommitteestatuses/", data = {
            "reviewCommitteeStatus" : "Status 1",
            "reviewCommitteeStatusDefinition" : "rc status def",
            "versionID" : 1,
        })
        self.assertEqual(response.json["reviewCommitteeStatusID"],1)
        self.assertEqual(response.json["reviewCommitteeStatus"],"Status 1")
        self.assertEqual(response.json["reviewCommitteeStatusDefinition"], "rc status def")
        self.assertEqual(response.json["versionID"],1)

class TestReviewCommittee(BlankDB):
    def setUp(self):
        db.drop_all()
        db.create_all()
        self.populate_db()

    def populate_db(self):
        p = models.Project(
            projectTypeID=1,
            irbHolderID=1,
            projectTitle="Test Project",
            shortTitle="Test Project",
            projectSummary="Summary",
            sop="sop",
            ucrProposal="ucr_proposal",
            budgetDoc="budget_doc",
            ucrFee="no",
            ucrNoFee="yes",
            previousShortTitle="t short",
            dateAdded=datetime(2016, 2, 2),
            finalRecruitmentReport="report",
            ongoingContact=True,
            activityStartDate=datetime(2016, 2, 2),
            activityEndDate=datetime(2016, 2, 2))

        db.session.add_all(self.create_irb_holders())
        db.session.add_all(self.create_project_types())
        db.session.add_all(self.create_review_committees())
        db.session.add_all(self.create_review_committee_statuses())
        db.session.add(p)
        db.session.commit()

    def test_empty_review_committee(self):
        response = self.client.get("/api/reviewcommittees/")
        self.assertEqual(response.json, dict(reviewCommittees = []))
        
    def test_review_committee_no_id(self):
        response = self.client.get("/api/reviewcommittees/1/")
        self.assertEqual(response.json, {"Error": "ReviewCommitteeID 1 not found"})
        
    def test_create_review_committee(self):
        response = self.client.post("/api/reviewcommittees/", data = {
            "projectID" : 1,
            "reviewCommitteeStatusID": 1,
            "reviewCommitteeLUTID": 1,
            "reviewCommitteeNumber":"1",
            "dateInitialReview":"2016-02-02",
            "dateExpires" : "2016-02-02",
            "rcNote" : "rc_note",
            "rcProtocol" : "rc_proto",
            "rcApproval":"rc_approval",
            "versionID" : 1,
        })
        self.assertEqual(response.json["reviewCommitteeID"],1)
        self.assertEqual(response.json["projectID"],1)
        self.assertEqual(response.json["reviewCommitteeStatusID"],1)
        self.assertEqual(response.json["reviewCommitteeNumber"],"1")
        self.assertEqual(response.json["dateInitialReview"],"2016-02-02")
        self.assertEqual(response.json["dateExpires"],"2016-02-02")
        self.assertEqual(response.json["rcNote"],"rc_note")
        self.assertEqual(response.json["rcProtocol"],"rc_proto")
        self.assertEqual(response.json["rcApproval"],"rc_approval")
        self.assertEqual(response.json["versionID"],1)

class TestReviewCommitteeLUT(BlankDB):
    def test_empty_review_committee_lists(self):
        response = self.client.get("/api/reviewcommitteelist/")
        self.assertEqual(response.json, dict(ReviewCommitteeList = []))
        
    def test_review_committee_list_no_id(self):
        response = self.client.get("/api/reviewcommitteelist/1/")
        self.assertEqual(response.json, {"Error": "ReviewCommitteeID 1 not found"})
        
    def test_create_review_committee_list(self):
        response = self.client.post("/api/reviewcommitteelist/", data = {
            "reviewCommittee" : "rc test",
            "reviewCommitteeDescription" : "rc desc",
            "versionID" : 1,
            })
        self.assertEqual(response.json["reviewCommitteeID"],1)
        self.assertEqual(response.json["reviewCommittee"],"rc test")
        self.assertEqual(response.json["reviewCommitteeDescription"],"rc desc")
        self.assertEqual(response.json["versionID"],1)

class TestStaff(BlankDB):

    def setUp(self):
        db.drop_all()
        db.create_all()
        self.populate_db()

    def populate_db(self):
        db.session.add_all(self.create_states())
        db.session.add_all(self.create_roles())
        db.session.add_all(self.create_users())
        db.session.add_all(self.create_ucr_roles())
        db.session.commit()

    def test_empty_staff(self):
        response = self.client.get("/api/staff/")
        self.assertEqual(response.json, dict(Staff = []))
        
    def test_staff_no_id(self):
        response = self.client.get("/api/staff/1/")
        self.assertEqual(response.json, {"Error": "StaffID 1 not found"})
        
    def test_create_staff(self):
        response = self.client.post("/api/staff/", data = {
            "firstName" : "fname",
            "lastName" : "lname",
            "middleName" : "middle_name",
            "email" : "email",
            "phoneNumber" : "phone",
            "phoneComment" : "phoneComment",
            "institution" : "institution",
            "department" : "department",
            "position" : "position",
            "credentials" : "credentials",
            "street" : "street",
            "city" : "city",
            "stateID" : 1,
            "ucrRoleID" : 1,
            "userID" : 1,
            "versionID" : 1,
            })
        self.assertEqual(response.json["staffID"],1)
        self.assertEqual(response.json["firstName"],"fname")
        self.assertEqual(response.json["lastName"],"lname")
        self.assertEqual(response.json["middleName"],"middle_name")
        self.assertEqual(response.json["email"],"email")
        self.assertEqual(response.json["phoneNumber"],"phone")
        self.assertEqual(response.json["phoneComment"],"phoneComment")
        self.assertEqual(response.json["institution"],"institution")
        self.assertEqual(response.json["department"],"department")
        self.assertEqual(response.json["position"],"position")
        self.assertEqual(response.json["credentials"],"credentials")
        self.assertEqual(response.json["street"],"street")
        self.assertEqual(response.json["city"],"city")
        self.assertEqual(response.json["stateID"],1)
        self.assertEqual(response.json["ucrRoleID"],1)
        self.assertEqual(response.json["userID"],1)
        self.assertEqual(response.json["versionID"],1)

class TestStaffRole(BlankDB):
    def test_empty_staff_role(self):
        response = self.client.get("/api/staffroles/")
        self.assertEqual(response.json, dict(StaffRoles = []))
        
    def test_staff_role_no_id(self):
        response = self.client.get("/api/staffroles/1/")
        self.assertEqual(response.json, {"Error": "StaffRoleID 1 not found"})
        
    def test_create_staff_role(self):
        response = self.client.post("/api/staffroles/", data = {
            "staffRole" : "role",
            "staffRoleDescription" : "desc",
            "versionID" : 1,
            })
        self.assertEqual(response.json["staffRoleID"],1)
        self.assertEqual(response.json["staffRole"],"role")
        self.assertEqual(response.json["staffRoleDescription"],"desc")
        self.assertEqual(response.json["versionID"],1)

class TestStaffTraining(BlankDB):
    def setUp(self):
        db.drop_all()
        db.create_all()
        self.populate_db()

    def populate_db(self):
        # Need to populate the FK tables with stuff
        staff = models.Staff(
            firstName = "fname",
            lastName = "lname",
            middleName = "middle_name",
            email = "email",
            phoneNumber = "phone",
            phoneComment = "phoneComment",
            institution = "institution",
            department = "department",
            position = "position",
            credentials = "credentials",
            street = "street",
            city = "city",
            stateID = 1,
            ucrRoleID = 1,
            userID = 1
        )
        db.session.add_all(self.create_states())
        db.session.add_all(self.create_roles())
        db.session.add_all(self.create_users())
        db.session.add_all(self.create_ucr_roles())
        db.session.add_all(self.create_human_subject_trainings())
        db.session.add(staff)
        db.session.commit()

    def test_empty_staff_training(self):
        response = self.client.get("/api/stafftrainings/")
        self.assertEqual(response.json, dict(StaffTrainings = []))
        
    def test_staff_training_no_id(self):
        response = self.client.get("/api/stafftrainings/1/")
        self.assertEqual(response.json, {"Error": "StaffTrainingID 1 not found"})
        
    def test_create_staff_training(self):
        response = self.client.post("/api/stafftrainings/", data = {
            "staffID" : 1,
            "humanSubjectTrainingID" : 1,
            "dateTaken" : "2016-02-02",
            "dateExpires" : "2016-02-02",
            "versionID" : 1,
            })
        self.assertEqual(response.json["staffTrainingID"],1)
        self.assertEqual(response.json["staffID"],1)
        self.assertEqual(response.json["humanSubjectTrainingID"],1)
        self.assertEqual(response.json["dateTaken"],"2016-02-02")
        self.assertEqual(response.json["dateExpires"],"2016-02-02")
        self.assertEqual(response.json["versionID"],1)

class TestTracing(BlankDB):
    def setUp(self):
        db.drop_all()
        db.create_all()
        self.populate_db()

    def populate_db(self):
        patient = models.Patient(
            patID="1",
            ucrDistID=1,
            UPDBID=1,
            firstName="fname2",
            lastName="lname2",
            middleName="mname2",
            maidenName="maiden_name",
            aliasFirstName="alias_fname",
            aliasLastName="alias_lname",
            aliasMiddleName="alias_middle",
            dobDay=26,
            dobMonth=4,
            dobYear=1970,
            SSN="999999999",
            sexID=1,
            raceID=2,
            ethnicityID=1,
            vitalStatusID=2
        )
        project1 = models.Project(
            projectTypeID=1,
            irbHolderID=1,
            projectTitle="Test Project",
            shortTitle="Test Project",
            projectSummary="Summary",
            sop="sop",
            ucrProposal="ucr_proposal",
            budgetDoc="budget_doc",
            ucrFee="no",
            ucrNoFee="yes",
            previousShortTitle="t short",
            dateAdded=datetime(2016, 2, 2),
            finalRecruitmentReport="report",
            ongoingContact=True,
            activityStartDate=datetime(2016, 2, 2),
            activityEndDate=datetime(2016, 2, 2))

        staff = models.Staff(
            userID=1,
            firstName="Aaron",
            lastName="Thomas",
            middleName="Pulver",
            email="aaron.pulver@utah.edu",
            phoneNumber="phone",
            phoneComment="phoneComment",
            institution="institution",
            department="department",
            position="position",
            credentials="credentials",
            street="street",
            city="city",
            stateID=1,
            ucrRoleID=1
        )

        ctc1 = models.CTC(
            participantID=1,
            dxDateDay=2,
            dxDateMonth=7,
            dxDateYear=1988,
            site="Site 2",
            histology="histology",
            behavior="behavior",
            ctcSequence="sequence",
            stage="stage",
            dxAge=1,
            dxStreet1="street1",
            dxStreet2="street2",
            dxCity="city",
            dxStateID=1,
            dxZip="99999",
            dxCounty="county",
            dnc="dnc",
            dncReason="dnc_reason",
            recordID="abc321"
        )

        projectPatient = models.ProjectPatient(
            projectID=1,
            staffID=1,
            ctcID=1,
            currentAge=1,
            batch=1,
            siteGrp=1,
            finalCodeID=1,
            finalCodeDate=datetime(2016, 2, 2),
            enrollmentDate=datetime(2016, 2, 2),
            dateCoordSigned=datetime(2016, 2, 2),
            importDate=datetime(2016, 2, 2),
            finalCodeStaffID=1,
            enrollmentStaffID=1,
            dateCoordSignedStaffID=1,
            abstractStatusID=1,
            abstractStatusDate=datetime(2016, 2, 2),
            abstractStatusStaffID=1,
            sentToAbstractorDate=datetime(2016, 2, 2),
            sentToAbstractorStaffID=1,
            abstractedDate=datetime(2016, 2, 2),
            abstractorStaffID=1,
            researcherDate=datetime(2016, 2, 2),
            researcherStaffID=1,
            consentLink="link",
            medRecordReleaseSigned=True,
            medRecordReleaseLink="link",
            medRecordReleaseStaffID=1,
            medRecordReleaseDate=datetime(2016, 2, 2),
            surveyToResearcher=datetime(2016, 2, 2),
            surveyToResearcherStaffID=1,
            qualityControl=True,
        )
        db.session.add_all(self.create_contact_types())
        db.session.add_all(self.create_sexes())
        db.session.add_all(self.create_races())
        db.session.add_all(self.create_ethnicities())
        db.session.add_all(self.create_vital_statuses())
        db.session.add_all(self.create_ucr_roles())
        db.session.add_all(self.create_final_codes())
        db.session.add_all(self.create_states())
        db.session.add_all(self.create_roles())
        db.session.add_all(self.create_users())
        db.session.add_all(self.create_irb_holders())
        db.session.add_all(self.create_project_types())
        db.session.add_all(self.create_abstract_statuses())
        db.session.add_all(self.create_tracing_sources())
        db.session.add(patient)
        db.session.add(staff)
        db.session.add(project1)
        db.session.add(ctc1)
        db.session.add(projectPatient)
        db.session.commit()

    def test_empty_tracing(self):
        response = self.client.get("/api/tracings/")
        self.assertEqual(response.json, dict(Tracings = []))
        
    def test_tracing_no_id(self):
        response = self.client.get("/api/tracings/1/")
        self.assertEqual(response.json, {"Error": "TracingID 1 not found"})
        
    def test_create_tracing(self):
        response = self.client.post("/api/tracings/", data = {
            "tracingSourceID" : 1,
            "participantID" : 1,
            "date" : "2016-02-02",
            "staffID" : 1,
            "notes" : "notes",
            "versionID" : 1,
            })
        self.assertEqual(response.json["tracingID"],1)
        self.assertEqual(response.json["participantID"],1)
        self.assertEqual(response.json["date"],"2016-02-02")
        self.assertEqual(response.json["staffID"],1)
        self.assertEqual(response.json["notes"],"notes")
        self.assertEqual(response.json["versionID"],1)

class TestTracingSource(BlankDB):
    def test_empty_tracing_source(self):
        response = self.client.get("/api/tracingsources/")
        self.assertEqual(response.json, dict(TracingSources = []))
        
    def test_tracing_source_no_id(self):
        response = self.client.get("/api/tracingsources/1/")
        self.assertEqual(response.json, {"Error": "TracingSourceID 1 not found"})
        
    def test_create_tracing_source(self):
        response = self.client.post("/api/tracingsources/", data = {
            "description" : "desc",
            "versionID" : 1,
            })
        self.assertEqual(response.json["tracingSourceID"],1)
        self.assertEqual(response.json["description"],"desc")
        self.assertEqual(response.json["versionID"],1)

class TestUCRReport(BlankDB):
    def setUp(self):
        db.drop_all()
        db.create_all()
        self.populate_db()

    def populate_db(self):
        p = models.Project(
            projectTypeID=1,
            irbHolderID=1,
            projectTitle="Test Project",
            shortTitle="Test Project",
            projectSummary="Summary",
            sop="sop",
            ucrProposal="ucr_proposal",
            budgetDoc="budget_doc",
            ucrFee="no",
            ucrNoFee="yes",
            previousShortTitle="t short",
            dateAdded=datetime(2016, 2, 2),
            finalRecruitmentReport="report",
            ongoingContact=True,
            activityStartDate=datetime(2016, 2, 2),
            activityEndDate=datetime(2016, 2, 2))

        db.session.add_all(self.create_irb_holders())
        db.session.add_all(self.create_project_types())
        db.session.add_all(self.create_ucr_report_types())
        db.session.add(p)
        db.session.commit()

    def test_empty_ucr_report(self):
        response = self.client.get("/api/ucrreports/")
        self.assertEqual(response.json, dict(ucrReports = []))
        
    def test_ucr_report_no_id(self):
        response = self.client.get("/api/ucrreports/1/")
        self.assertEqual(response.json, {"Error": "UcrReportID 1 not found"})
        
    def test_create_ucr_report(self):
        response = self.client.post("/api/ucrreports/", data = {
            "projectID" : 1,
            "reportTypeID" : 1,
            "reportSubmitted" : "2016-02-02",
            "reportDue" : "2016-02-02",
            "reportDoc" : "doc",
            "versionID" : 1,
        })
        self.assertEqual(response.json["ucrReportID"],1)
        self.assertEqual(response.json["projectID"],1)
        self.assertEqual(response.json["reportTypeID"],1)
        self.assertEqual(response.json["reportSubmitted"],"2016-02-02")
        self.assertEqual(response.json["reportDue"],"2016-02-02")
        self.assertEqual(response.json["reportDoc"],"doc")
        self.assertEqual(response.json["versionID"],1)

class TestUCRRole(BlankDB):

    def test_empty_ucr_report(self):
        response = self.client.get("/api/ucrroles/")
        self.assertEqual(response.json, dict(ucrRoles = []))

    def test_ucr_role_no_id(self):
        response = self.client.get("/api/ucrroles/1/")
        self.assertEqual(response.json, {"Error": "UCRRoleID 1 not found"})

    def test_create_ucr_role(self):
        response = self.client.post("/api/ucrroles/", data={
            "ucrRole": "role"
        })
        self.assertEqual(response.json["ucrRoleID"],1)
        self.assertEqual(response.json["ucrRole"],"role")

if __name__ == '__main__':
    unittest.main()
    