"""
    This is a stand-a-lone script that can seed the database for ad-hoc testing
"""

from flask import Flask
import app
from app.database import db
from datetime import datetime
import app.models as models


def create_informant_relationships():
    relationships = []
    relationships.append(models.InformantRelationship(
        informantRelationship="Spouse/Partner",
        informantRelationshipID=0
    ))
    relationships.append(models.InformantRelationship(
        informantRelationship="Ex-spouse",
        informantRelationshipID=1
    ))
    relationships.append(models.InformantRelationship(
        informantRelationship="Child",
        informantRelationshipID=10
    ))
    relationships.append(models.InformantRelationship(
        informantRelationship="In-Law",
        informantRelationshipID=5
    ))
    relationships.append(models.InformantRelationship(
        informantRelationship="Ex-In-law",
        informantRelationshipID=6
    ))
    relationships.append(models.InformantRelationship(
        informantRelationship="Grandchild",
        informantRelationshipID=12
    ))
    relationships.append(models.InformantRelationship(
        informantRelationship="Nephew/Niece",
        informantRelationshipID=14
    ))
    relationships.append(models.InformantRelationship(
        informantRelationship="Parent",
        informantRelationshipID=20
    ))
    relationships.append(models.InformantRelationship(
        informantRelationship="Step-parent",
        informantRelationshipID=21
    ))
    relationships.append(models.InformantRelationship(
        informantRelationship="Guardian",
        informantRelationshipID=22
    ))
    relationships.append(models.InformantRelationship(
        informantRelationship="Grandparent",
        informantRelationshipID=23
    ))
    relationships.append(models.InformantRelationship(
        informantRelationship="Aunt/Uncle",
        informantRelationshipID=24
    ))
    relationships.append(models.InformantRelationship(
        informantRelationship="Sibling",
        informantRelationshipID=30
    ))
    relationships.append(models.InformantRelationship(
        informantRelationship="Other Relative",
        informantRelationshipID=39
    ))
    relationships.append(models.InformantRelationship(
        informantRelationship="Friend/Neighbor",
        informantRelationshipID=40
    ))
    relationships.append(models.InformantRelationship(
        informantRelationship="Boyfriend/Girlfriend",
        informantRelationshipID=41
    ))
    relationships.append(models.InformantRelationship(
        informantRelationship="Employer",
        informantRelationshipID=50
    ))
    relationships.append(models.InformantRelationship(
        informantRelationship="Attorney",
        informantRelationshipID=60
    ))
    relationships.append(models.InformantRelationship(
        informantRelationship="Power of Attorney",
        informantRelationshipID=61
    ))
    relationships.append(models.InformantRelationship(
        informantRelationship="Doctor",
        informantRelationshipID=70
    ))
    relationships.append(models.InformantRelationship(
        informantRelationship="Caregiver",
        informantRelationshipID=71
    ))
    relationships.append(models.InformantRelationship(
        informantRelationship="Other",
        informantRelationshipID=88
    ))
    relationships.append(models.InformantRelationship(
        informantRelationship="Unknown",
        informantRelationshipID=99
    ))


    return relationships


def create_final_codes():
    finalCodes = []
    finalCodes.append(models.FinalCode(
        finalCodeDefinition="Pending",
        finalCode=0,
        finalCodeID=1
    ))
    finalCodes.append(models.FinalCode(
        finalCodeDefinition="Consent- Survey complete w/Med. Rcd. release",
        finalCode=100,
        finalCodeID=2
    ))
    finalCodes.append(models.FinalCode(
        finalCodeDefinition="Consent- Survey complete NO Med.Rcd. release",
        finalCode=101,
        finalCodeID=3
    ))
    finalCodes.append(models.FinalCode(
        finalCodeDefinition="Consent- Incomplete survey. Cannot complete (see notes for reason)",
        finalCode=111,
        finalCodeID=4
    ))
    finalCodes.append(models.FinalCode(
        finalCodeDefinition="Survey complete- no consent form with or without medical release",
        finalCode=112,
        finalCodeID=5
    ))
    finalCodes.append(models.FinalCode(
        finalCodeDefinition="No- by mail",
        finalCode=200,
        finalCodeID=6
    ))
    finalCodes.append(models.FinalCode(
        finalCodeDefinition="No- no reason",
        finalCode=201,
        finalCodeID=7

    ))
    finalCodes.append(models.FinalCode(
        finalCodeDefinition="No- too ill",
        finalCode=202,
        finalCodeID=8
    ))
    finalCodes.append(models.FinalCode(
        finalCodeDefinition="No- no interest",
        finalCode=203,
        finalCodeID=9
    ))
    finalCodes.append(models.FinalCode(
        finalCodeDefinition="No- too old",
        finalCode=204,
        finalCodeID=10
    ))
    finalCodes.append(models.FinalCode(
        finalCodeDefinition="No- no cancer",
        finalCode=205,
        finalCodeID=11
    ))
    finalCodes.append(models.FinalCode(
        finalCodeDefinition="No-upset",
        finalCode=207,
        finalCodeID=12
    ))
    finalCodes.append(models.FinalCode(
        finalCodeDefinition="No- DO NOT CONTACT-per contact with patient on study",
        finalCode=208,
        finalCodeID=13
    ))
    finalCodes.append(models.FinalCode(
        finalCodeDefinition="No- no signed consent form",
        finalCode=209,
        finalCodeID=14
    ))
    finalCodes.append(models.FinalCode(
        finalCodeDefinition="No response after max effort",
        finalCode=300,
        finalCodeID=15
    ))
    finalCodes.append(models.FinalCode(
        finalCodeDefinition="Lost to follow-up (bad/no address or phone)-may have contacted once or initial letter not returned, but can no longer contact",
        finalCode=301,
        finalCodeID=16
    ))
    finalCodes.append(models.FinalCode(
        finalCodeDefinition="Language Barrier",
        finalCode=302,
        finalCodeID=17
    ))
    finalCodes.append(models.FinalCode(
        finalCodeDefinition="No response after 2+ letters (no/bad phone)",
        finalCode=303,
        finalCodeID=18
    ))
    finalCodes.append(models.FinalCode(
        finalCodeDefinition="Deceased AFTER selection",
        finalCode=309,
        finalCodeID=19
    ))
    finalCodes.append(models.FinalCode(
        finalCodeDefinition="Ineligible - Current Age",
        finalCode=400,
        finalCodeID=20
    ))
    finalCodes.append(models.FinalCode(
        finalCodeDefinition="Ineligible-other",
        finalCode=401,
        finalCodeID=21
    ))
    finalCodes.append(models.FinalCode(
        finalCodeDefinition="Ineligible- DX date",
        finalCode=402,
        finalCodeID=22
    ))
    finalCodes.append(models.FinalCode(
        finalCodeDefinition="Ineligible- Patient Deceased",
        finalCode=403,
        finalCodeID=23
    ))
    finalCodes.append(models.FinalCode(
        finalCodeDefinition="Ineligible- mental capacity",
        finalCode=404,
        finalCodeID=24
    ))
    finalCodes.append(models.FinalCode(
        finalCodeDefinition="Ineligible- histology or behavior",
        finalCode=406,
        finalCodeID=25
    ))
    finalCodes.append(models.FinalCode(
        finalCodeDefinition="Ineligible- out of state resident at DX",
        finalCode=407,
        finalCodeID=26
    ))
    finalCodes.append(models.FinalCode(
        finalCodeDefinition="Ineligible-Recently contacted for another UCR study or lost to follow-up in another UCR study within past year",
        finalCode=408,
        finalCodeID=27
    ))
    finalCodes.append(models.FinalCode(
        finalCodeDefinition="Ineligible-out of country",
        finalCode=409,
        finalCodeID=28
    ))
    finalCodes.append(models.FinalCode(
        finalCodeDefinition="Ineligible-Do not contact per DMS",
        finalCode=410,
        finalCodeID=29
    ))
    finalCodes.append(models.FinalCode(
        finalCodeDefinition="Ineligible-Not able to send letter OR letter returned and no other contact possible (for NOK or Patient)",
        finalCode=411,
        finalCodeID=30
    ))
    finalCodes.append(models.FinalCode(
        finalCodeDefinition="Ineligible - Contacted for other study within 1 year",
        finalCode=412,
        finalCodeID=31
    ))
    finalCodes.append(models.FinalCode(
        finalCodeDefinition="Holding",
        finalCode=999,
        finalCodeID=32
    ))
    return finalCodes


def create_states():
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


def create_abstract_statuses():
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


def create_sexes():
    sexes = []
    sexes.append(models.Sex(
        sex="Female",
        sexID=2
    ))
    sexes.append(models.Sex(
        sex="Male",
        sexID=1
    ))
    sexes.append(models.Sex(
        sex="Transsexual, NOS",
        sexID=4
    ))
    sexes.append(models.Sex(
        sex="Transsexual, natal male",
        sexID=5
    ))
    sexes.append(models.Sex(
        sex="Transsexual, natal female",
        sexID=6
    ))
    sexes.append(models.Sex(
        sex="Not stated/Unknown",
        sexID=9
    ))
    sexes.append(models.Sex(
        sex="Other (intersex, disorders of sexual development/DSD)",
        sexID=3
    ))
    return sexes

def create_sitegroup():
    sitegroups = []
    sitegroups.append(models.SiteGroup(
        site="Breast Cancer"
    ))
    sitegroups.append(models.SiteGroup(
        site="Colon Cancer"
    ))
    sitegroups.append(models.SiteGroup(
        site="Liver Cancer"
    ))
    sitegroups.append(models.SiteGroup(
        site="Unknown"
    ))
    return sitegroups

def create_races():
    races = []
    races.append(models.Race(
        race="White",
        raceID=1
    ))
    races.append(models.Race(
        race="Black",
        raceID=2
    ))
    races.append(models.Race(
        race="American Indian/Alaska Native",
        raceID=3
    ))
    races.append(models.Race(
        race="Chinese",
        raceID=4
    ))
    races.append(models.Race(
        race="Japanese",
        raceID=5
    ))
    races.append(models.Race(
        race="Filipino",
        raceID=6
    ))
    races.append(models.Race(
        race="Hawaiian",
        raceID=7
    ))
    races.append(models.Race(
        race="Korean",
        raceID=8
    ))
    races.append(models.Race(
        race="Vietnamese",
        raceID=10
    ))
    races.append(models.Race(
        race="Laotian",
        raceID=11
    ))
    races.append(models.Race(
        race="Hmong",
        raceID=12
    ))
    races.append(models.Race(
        race="Kampuchean (Cambodian)",
        raceID=13
    ))
    races.append(models.Race(
        race="Thai",
        raceID=14
    ))
    races.append(models.Race(
        race="Asian Indian, Pakistani, NOS",
        raceID=15
    ))
    races.append(models.Race(
        race="Asian Indian",
        raceID=16
    ))
    races.append(models.Race(
        race="Pakistani",
        raceID=17
    ))
    races.append(models.Race(
        race="Micronesian, NOS",
        raceID=20
    ))
    races.append(models.Race(
        race="Chamorro/Chamoru",
        raceID=21
    ))
    races.append(models.Race(
        race="Guamanian, NOS",
        raceID=22
    ))
    races.append(models.Race(
        race="Polynesian, NOS",
        raceID=25
    ))
    races.append(models.Race(
        race="Tahitian",
        raceID=26
    ))
    races.append(models.Race(
        race="Samoan",
        raceID=27
    ))
    races.append(models.Race(
        race="Tongan",
        raceID=28
    ))
    races.append(models.Race(
        race="Melanesian, NOS",
        raceID=30
    ))
    races.append(models.Race(
        race="Fiji Islander",
        raceID=31
    ))
    races.append(models.Race(
        race="New Guinean",
        raceID=32
    ))
    races.append(models.Race(
        race="No further race documented",
        raceID=88
    ))
    races.append(models.Race(
        race="Other Asian",
        raceID=96
    ))
    races.append(models.Race(
        race="Pacific Islander, NOS",
        raceID=97
    ))
    races.append(models.Race(
        race="Other",
        raceID=98
    ))
    races.append(models.Race(
        race="Unknown",
        raceID=99
    ))
    return races


def create_ethnicities():
    ethnicities = []
    ethnicities.append(models.Ethnicity(
        ethnicity="Non-Spanish",
        ethnicityID=0
    ))
    ethnicities.append(models.Ethnicity(
        ethnicity="Mexican",
        ethnicityID=1
    ))
    ethnicities.append(models.Ethnicity(
        ethnicity="Puerto Rican",
        ethnicityID=2
    ))
    ethnicities.append(models.Ethnicity(
        ethnicity="Cuban",
        ethnicityID=3
    ))
    ethnicities.append(models.Ethnicity(
        ethnicity="South or Central American (except Brazil)",
        ethnicityID=4
    ))
    ethnicities.append(models.Ethnicity(
        ethnicity="Other Spanish",
        ethnicityID=5
    ))
    ethnicities.append(models.Ethnicity(
        ethnicity="Spanish, NOS",
        ethnicityID=6
    ))
    ethnicities.append(models.Ethnicity(
        ethnicity="Spanish surname only",
        ethnicityID=7
    ))
    ethnicities.append(models.Ethnicity(
        ethnicity="Dominican Republic (2005+)",
        ethnicityID=8
    ))
    ethnicities.append(models.Ethnicity(
        ethnicity="Unknown",
        ethnicityID=9
    ))

    return ethnicities


def create_vital_statuses():
    vitals = []
    vitals.append(models.VitalStatus(
        vitalStatus="Alive",
        vitalStatusID=1
    ))
    vitals.append(models.VitalStatus(
        vitalStatus="Dead",
        vitalStatusID=4
    ))
    return vitals


def create_contacts():
    contacts = []
    contacts.append(models.Contacts(
        contact="Yes"
    ))
    contacts.append(models.Contacts(
        contact="No"
    ))
    return contacts


def create_inactives():
    inactives = []
    inactives.append(models.Inactive(
        inactive="Yes"
    ))
    inactives.append(models.Inactive(
        inactive="No"
    ))
    return inactives


def create_ucr_report_types():
    reports = []
    reports.append(models.UCRReportType(
        ucrReportType="Final Report"
    ))
    reports.append(models.UCRReportType(
        ucrReportType="Annual Report"
    ))
    return reports


def create_physician_statuses():
    statuses = []
    statuses.append(models.PhysicianStatus(
        physicianStatus="Active"
    ))
    statuses.append(models.PhysicianStatus(
        physicianStatus="Inactive"
    ))
    return statuses


def create_physician_facility_statuses():
    statuses = []
    statuses.append(models.PhysicianFacilityStatus(
        physicianFacilityStatus="Open"
    ))
    statuses.append(models.PhysicianFacilityStatus(
        physicianFacilityStatus="Closed"
    ))
    return statuses


def create_phone_types():
    phoneTypes = []
    phoneTypes.append(models.PhoneTypeLUT(
        phoneType="Cell"
    ))
    phoneTypes.append(models.PhoneTypeLUT(
        phoneType="Home"
    ))
    phoneTypes.append(models.PhoneTypeLUT(
        phoneType="Work"
    ))
    return phoneTypes


def create_irb_holders():
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


def create_project_types():
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


def create_contact_statuses():
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


def create_contact_sources():
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


def create_grant_statuses():
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


def create_funding_sources():
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


def create_review_committee_statuses():
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


def create_project_statuses():
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


def create_log_subjects():
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


def create_review_committees():
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


def create_staff_roles():
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


def create_project_phases():
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


def create_human_subject_trainings():
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


def create_tracing_sources():
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


def create_contact_types():
    contact_types = []
    contact_types.append(models.ContactTypeLUT(
        contactDefinition="Mailed 1st packet to patient (intro letter, survey, consent, med rcd. release)",
        contactCode=100,
        contactTypeID=1
    ))
    contact_types.append(models.ContactTypeLUT(
        contactDefinition="Mailed Reminder letter",
        contactCode=101,
        contactTypeID=2
    ))
    contact_types.append(models.ContactTypeLUT(
        contactDefinition="Mailed 2nd packet (FU letter, survey, consent, med rcd release)",
        contactCode=102,
        contactTypeID=3
    ))
    contact_types.append(models.ContactTypeLUT(
        contactDefinition="Mailed Thank you letter and copy of consent form",
        contactCode=103,
        contactTypeID=4
    ))
    contact_types.append(models.ContactTypeLUT(
        contactDefinition="Mailed Packet (after phone contact)",
        contactCode=109,
        contactTypeID=9
    ))
    contact_types.append(models.ContactTypeLUT(
        contactDefinition="Mailed additional items- (survey, consent form, envelope, etc)",
        contactCode=110,
        contactTypeID=89
    ))
    contact_types.append(models.ContactTypeLUT(
        contactDefinition="Undeliverable, mail returned w/forwarding addresses, mailed to new address",
        contactCode=150,
        contactTypeID=45
    ))
    contact_types.append(models.ContactTypeLUT(
        contactDefinition="Undeliverable, Mail returned, NO forwarding address",
        contactCode=151,
        contactTypeID=576
    ))
    contact_types.append(models.ContactTypeLUT(
        contactDefinition="Packet Returned - Temporarily Away",
        contactCode=152,
        contactTypeID=98
    ))
    contact_types.append(models.ContactTypeLUT(
        contactDefinition="Left voicemail",
        contactCode=200,
        contactTypeID=34
    ))
    contact_types.append(models.ContactTypeLUT(
        contactDefinition="Left message with person",
        contactCode=201,
        contactTypeID=12
    ))
    contact_types.append(models.ContactTypeLUT(
        contactDefinition="No answer",
        contactCode=202,
        contactTypeID=485
    ))
    contact_types.append(models.ContactTypeLUT(
        contactDefinition="Busy",
        contactCode=203,
        contactTypeID=344
    ))
    contact_types.append(models.ContactTypeLUT(
        contactDefinition="Bad Phone number",
        contactCode=204,
        contactTypeID=122
    ))
    contact_types.append(models.ContactTypeLUT(
        contactDefinition="Spoke with- Received, thinking about it",
        contactCode=205,
        contactTypeID=67
    ))
    contact_types.append(models.ContactTypeLUT(
        contactDefinition="Spoke with- Received, willing",
        contactCode=206,
        contactTypeID=123
    ))
    contact_types.append(models.ContactTypeLUT(
        contactDefinition="Spoke with- Received, already sent to us",
        contactCode=207,
        contactTypeID=16

    ))
    contact_types.append(models.ContactTypeLUT(
        contactDefinition="Spoke with- too sick",
        contactCode=208,
        contactTypeID=17
    ))
    contact_types.append(models.ContactTypeLUT(
        contactDefinition="Spoke with- no cancer",
        contactCode=209,
        contactTypeID=18
    ))
    contact_types.append(models.ContactTypeLUT(
        contactDefinition="Language Barrier",
        contactCode=210,
        contactTypeID=20
    ))
    contact_types.append(models.ContactTypeLUT(
        contactDefinition="Deceased",
        contactCode=211,
        contactTypeID=21
    ))
    contact_types.append(models.ContactTypeLUT(
        contactDefinition="Pt unable to come to phone, could not leave message",
        contactCode=212,
        contactTypeID=22
    ))
    contact_types.append(models.ContactTypeLUT(
        contactDefinition="Incompetent",
        contactCode=213,
        contactTypeID=44
    ))
    contact_types.append(models.ContactTypeLUT(
        contactDefinition="Patient left message for Coordinator",
        contactCode=214,
        contactTypeID=55
    ))
    contact_types.append(models.ContactTypeLUT(
        contactDefinition="Spoke with- Refused (no reason given)",
        contactCode=215,
        contactTypeID=66
    ))
    contact_types.append(models.ContactTypeLUT(
        contactDefinition="Ineligible",
        contactCode=216,
        contactTypeID=77
    ))
    contact_types.append(models.ContactTypeLUT(
        contactDefinition="Spoke with- did not receive, mailed another letter",
        contactCode=217,
        contactTypeID=333
    ))
    contact_types.append(models.ContactTypeLUT(
        contactDefinition="Spoke with- Other",
        contactCode=218,
        contactTypeID=444
    ))
    contact_types.append(models.ContactTypeLUT(
        contactDefinition="Survey returned without consent form",
        contactCode=300,
        contactTypeID=222
    ))
    contact_types.append(models.ContactTypeLUT(
        contactDefinition="Survey returned incomplete",
        contactCode=301,
        contactTypeID=999
    ))
    contact_types.append(models.ContactTypeLUT(
        contactDefinition="Consent returned without survey",
        contactCode=302,
        contactTypeID=345
    ))
    contact_types.append(models.ContactTypeLUT(
        contactDefinition="Received consent, survey received previously",
        contactCode=304,
        contactTypeID=789
    ))
    contact_types.append(models.ContactTypeLUT(
        contactDefinition="Enter in error",
        contactCode=999,
        contactTypeID=356
    ))
    return contact_types


def create_ucr_roles():
    roles = []
    roles.append(models.UCRRole(
        ucrRole="Contact Staff"
    ))
    roles.append(models.UCRRole(
        ucrRole="Developer"
    ))
    roles.append(models.UCRRole(
        ucrRole="Director"
    ))
    roles.append(models.UCRRole(
        ucrRole="Informatics Staff"
    ))
    roles.append(models.UCRRole(
        ucrRole="Research Manager"
    ))
    return roles


def create_gift_cards():
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
    gcs.append(models.GiftCard(
        description="Smiths Gift Card",
        barcode="123456786",
        amount=25
    ))
    gcs.append(models.GiftCard(
        description="Smiths Gift Card",
        barcode="123456785",
        amount=25
    ))
    gcs.append(models.GiftCard(
        description="Smiths Gift Card",
        barcode="123456784",
        amount=25
    ))
    gcs.append(models.GiftCard(
        description="Smiths Gift Card",
        barcode="123456783",
        amount=25
    ))
    gcs.append(models.GiftCard(
        description="Smiths Gift Card",
        barcode="123456782",
        amount=25
    ))
    gcs.append(models.GiftCard(
        description="Smiths Gift Card",
        barcode="123456781",
        amount=25
    ))
    gcs.append(models.GiftCard(
        description="Smiths Gift Card",
        barcode="123456780",
        amount=25
    ))
    return gcs


def create_users():
    users = []
    users.append(models.User(
        uID="u0973461",
    ))
    users.append(models.User(
        uID="u0050151",
    ))
    users.append(models.User(
        uID="u0372607",
    ))
    users.append(models.User(
        uID="u0710561",
    ))
    users.append(models.User(
        uID="u0100768",
    ))
    users.append(models.User(
        uID="u0030586",
    ))
    users.append(models.User(
        uID="u0666687",
    ))
    return users


def create_staff():
    staff = []
    staff.append(models.Staff(
        userID=1,
        firstName="Aaron",
        lastName="Pulver",
        middleName="Thomas",
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
        ucrRoleID=2
    ))
    staff.append(models.Staff(
        userID=2,
        firstName="Phoebe",
        lastName="McNeally",
        middleName="",
        email="phoebe.mcneally.geog.utah.edu",
        phoneNumber="phone",
        phoneComment="phoneComment",
        institution="institution",
        department="department",
        position="position",
        credentials="credentials",
        street="street",
        city="city",
        stateID=2,
        ucrRoleID=2
    ))
    staff.append(models.Staff(
        userID=3,
        firstName="Carrie",
        lastName="Bateman",
        middleName="",
        email="u0372607@utah.edu",
        phoneNumber="phone",
        phoneComment="phoneComment",
        institution="institution",
        department="department",
        position="position",
        credentials="credentials",
        street="street",
        city="city",
        stateID=2,
        ucrRoleID=4
    ))
    staff.append(models.Staff(
        userID=4,
        firstName="Valerie",
        lastName="Otto",
        middleName="Yoder",
        email="u0710561@utah.edu",
        phoneNumber="phone",
        phoneComment="phoneComment",
        institution="institution",
        department="department",
        position="position",
        credentials="credentials",
        street="street",
        city="city",
        stateID=2,
        ucrRoleID=5
    ))
    staff.append(models.Staff(
        userID=5,
        firstName="Kate",
        lastName="Hak",
        middleName="",
        email="u0372607@utah.edu",
        phoneNumber="phone",
        phoneComment="phoneComment",
        institution="institution",
        department="department",
        position="position",
        credentials="credentials",
        street="street",
        city="city",
        stateID=2,
        ucrRoleID=5
    ))
    staff.append(models.Staff(
        userID=6,
        firstName="Sandie",
        lastName="Edwards",
        middleName="",
        email="u0030586@utah.edu",
        phoneNumber="phone",
        phoneComment="phoneComment",
        institution="institution",
        department="department",
        position="position",
        credentials="credentials",
        street="street",
        city="city",
        stateID=2,
        ucrRoleID=1
    ))
    staff.append(models.Staff(
        userID=7,
        firstName="Lori",
        lastName="Burke",
        middleName="",
        email="u0666687@utah.edu",
        phoneNumber="phone",
        phoneComment="phoneComment",
        institution="institution",
        department="department",
        position="position",
        credentials="credentials",
        street="street",
        city="city",
        stateID=2,
        ucrRoleID=1
    ))
    return staff


def create_projects():
    projects = []
    projects.append(
        models.Project(
            projectTypeID=1,
            irbHolderID=1,
            projectTitle="Test Project 1",
            shortTitle="Test Project 1",
            projectSummary="Summary of Project 1",
            sop="sop",
            ucrProposal="UCR Proposal 1",
            budgetDoc="N:/Fakelocation/fakebudget.pdf",
            ucrFee=34.5,
            ucrNoFee=True,
            previousShortTitle="Test Project One",
            dateAdded=datetime(2016, 2, 2),
            finalRecruitmentReport="N:/Fakelocation/fakereport.pdf",
            ongoingContact=True,
            activityStartDate=datetime(2016, 2, 2),
            activityEndDate=datetime(2016, 2, 2),
            numberAbstractions=6,
            irbResearchManager=0,
            sftpUsername = 'r548363'
        )
    )
    projects.append(
        models.Project(
            projectTypeID=2,
            irbHolderID=2,
            projectTitle="Test Project 2",
            shortTitle="Test Project 2",
            projectSummary="Summary of Project 2",
            sop="sop",
            ucrProposal="UCR Proposal 2",
            budgetDoc="N:/Fakelocation/fakebudget2.pdf",
            ucrFee=345.78,
            ucrNoFee=False,
            previousShortTitle="Test Project Two",
            dateAdded=datetime(2016, 2, 2),
            finalRecruitmentReport="N:/Fakelocation/fakereport2.pdf",
            ongoingContact=True,
            activityStartDate=datetime(2016, 2, 2),
            activityEndDate=datetime(2016, 2, 2),
            numberAbstractions=89,
            sftpUsername='F587385',
            irbResearchManager=0
        )
    )
    projects.append(
        models.Project(
            projectTypeID=3,
            irbHolderID=3,
            projectTitle="Test Project 3",
            shortTitle="Test Project 3",
            projectSummary="Summary of Project 3",
            sop="sop",
            ucrProposal="UCR Proposal 3",
            budgetDoc="N:/Fakelocation/fakebudget3.pdf",
            ucrFee=1.24,
            ucrNoFee=True,
            previousShortTitle="Test Project Three",
            dateAdded=datetime(2016, 4, 5),
            finalRecruitmentReport="N:/Fakelocation/fakereport3.pdf",
            ongoingContact=True,
            activityStartDate=datetime(2016, 4, 5),
            activityEndDate=datetime(2016, 6, 7),
            numberAbstractions=456,
            sftpUsername='komaster',
            irbResearchManager=0

        )
    )
    projects.append(
        models.Project(
            projectTypeID=1,
            irbHolderID=4,
            projectTitle="Test Project 4",
            shortTitle="Test Project 4",
            projectSummary="Summary of Project 4",
            sop="sop",
            ucrProposal="UCR Proposal 4",
            budgetDoc="N:/Fakelocation/fakebudget4.pdf",
            ucrFee=4567.09,
            ucrNoFee=False,
            previousShortTitle="Test Project Four",
            dateAdded=datetime(2016, 8, 8),
            finalRecruitmentReport="N:/Fakelocation/fakereport4.pdf",
            ongoingContact=True,
            activityStartDate=datetime(2016, 9, 9),
            activityEndDate=datetime(2016, 9, 10),
            numberAbstractions=56,
            sftpUsername='classic',
            irbResearchManager=1
        )
    )
    projects.append(
        models.Project(
            projectTypeID=2,
            irbHolderID=3,
            projectTitle="Test Project 5",
            shortTitle="Test Project 5",
            projectSummary="Summary of Project 5",
            sop="sop",
            ucrProposal="UCR Proposal 2",
            budgetDoc="N:/Fakelocation/fakebudget5.pdf",
            ucrFee=76.45,
            ucrNoFee=True,
            previousShortTitle="Test Project Five",
            dateAdded=datetime(2016, 2, 2),
            finalRecruitmentReport="N:/Fakelocation/fakereport5.pdf",
            ongoingContact=True,
            activityStartDate=datetime(2016, 2, 2),
            activityEndDate=datetime(2016, 2, 2),
            numberAbstractions=436,
            sftpUsername='aniMation',
            irbResearchManager=0

        )
    )
    return projects


def create_budgets():
    budgets = []
    budgets.append(
        models.Budget(
            projectID=1,
            numPeriods=1,
            periodStart=datetime(2016, 2, 2),
            periodEnd=datetime(2016, 9, 9),
            periodTotal=1000,
            periodComment="Initial Budget"))
    budgets.append(
        models.Budget(
            projectID=1,
            numPeriods=1,
            periodStart=datetime(2016, 9, 10),
            periodEnd=datetime(2016, 12, 31),
            periodTotal=1000,
            periodComment="Second Budget"))
    budgets.append(
        models.Budget(
            projectID=2,
            numPeriods=1,
            periodStart=datetime(2016, 2, 2),
            periodEnd=datetime(2016, 9, 9),
            periodTotal=1000,
            periodComment="Initial Budget"))
    budgets.append(
        models.Budget(
            projectID=2,
            numPeriods=1,
            periodStart=datetime(2016, 9, 10),
            periodEnd=datetime(2016, 12, 31),
            periodTotal=1000,
            periodComment="Second Budget"))
    budgets.append(
        models.Budget(
            projectID=3,
            numPeriods=1,
            periodStart=datetime(2016, 2, 2),
            periodEnd=datetime(2016, 9, 9),
            periodTotal=1000,
            periodComment="Initial Budget"))
    budgets.append(
        models.Budget(
            projectID=3,
            numPeriods=1,
            periodStart=datetime(2016, 9, 10),
            periodEnd=datetime(2016, 12, 31),
            periodTotal=1000,
            periodComment="Second Budget"))
    budgets.append(
        models.Budget(
            projectID=4,
            numPeriods=1,
            periodStart=datetime(2016, 2, 2),
            periodEnd=datetime(2016, 9, 9),
            periodTotal=1000,
            periodComment="Initial Budget"))
    budgets.append(
        models.Budget(
            projectID=4,
            numPeriods=1,
            periodStart=datetime(2016, 9, 10),
            periodEnd=datetime(2016, 12, 31),
            periodTotal=1000,
            periodComment="Second Budget"))
    budgets.append(
        models.Budget(
            projectID=5,
            numPeriods=1,
            periodStart=datetime(2016, 2, 2),
            periodEnd=datetime(2016, 9, 9),
            periodTotal=1000,
            periodComment="Initial Budget"))
    budgets.append(
        models.Budget(
            projectID=5,
            numPeriods=1,
            periodStart=datetime(2016, 9, 10),
            periodEnd=datetime(2016, 12, 31),
            periodTotal=1000,
            periodComment="Second Budget"))
    return budgets


def create_project_review_committees():
    rcs = []
    rcs.append(models.ReviewCommittee(
        projectID=1,
        reviewCommitteeStatusID=1,
        reviewCommitteeLUTID=1,
        reviewCommitteeNumber="1",
        dateInitialReview=datetime(2016, 2, 2),
        dateExpires=datetime(2016, 10, 10),
        rcNote="Notes",
        rcProtocol="Protocol 1",
        rcApproval="No"))
    rcs.append(models.ReviewCommittee(
        projectID=1,
        reviewCommitteeStatusID=2,
        reviewCommitteeLUTID=2,
        reviewCommitteeNumber="2",
        dateInitialReview=datetime(2016, 2, 2),
        dateExpires=datetime(2016, 10, 10),
        rcNote="Notes",
        rcProtocol="Protocol 1",
        rcApproval="Approved"))
    rcs.append(models.ReviewCommittee(
        projectID=2,
        reviewCommitteeStatusID=2,
        reviewCommitteeLUTID=2,
        reviewCommitteeNumber="3",
        dateInitialReview=datetime(2016, 2, 2),
        dateExpires=datetime(2016, 10, 10),
        rcNote="Notes",
        rcProtocol="Protocol 1",
        rcApproval="Approved"))
    rcs.append(models.ReviewCommittee(
        projectID=2,
        reviewCommitteeStatusID=3,
        reviewCommitteeLUTID=3,
        reviewCommitteeNumber="4",
        dateInitialReview=datetime(2016, 2, 2),
        dateExpires=datetime(2016, 10, 10),
        rcNote="Notes",
        rcProtocol="Protocol 1",
        rcApproval="Approved"))
    rcs.append(models.ReviewCommittee(
        projectID=3,
        reviewCommitteeStatusID=1,
        reviewCommitteeLUTID=1,
        reviewCommitteeNumber="5",
        dateInitialReview=datetime(2016, 2, 2),
        dateExpires=datetime(2016, 10, 10),
        rcNote="Notes",
        rcProtocol="Protocol 1",
        rcApproval="No"))
    rcs.append(models.ReviewCommittee(
        projectID=4,
        reviewCommitteeStatusID=2,
        reviewCommitteeLUTID=2,
        reviewCommitteeNumber="6",
        dateInitialReview=datetime(2016, 2, 2),
        dateExpires=datetime(2016, 10, 10),
        rcNote="Notes",
        rcProtocol="Protocol 1",
        rcApproval="Approved"))
    return rcs


def create_ucr_reports():
    ucr_reports = []
    ucr_reports.append(models.UCRReport(
        projectID=1,
        reportTypeID=1,
        reportSubmitted=datetime(2016, 2, 2),
        reportDue=datetime(2016, 2, 2),
        reportDoc="N:/FakeLocation/FakeDoc1.pdf"
    ))
    ucr_reports.append(models.UCRReport(
        projectID=2,
        reportTypeID=1,
        reportSubmitted=datetime(2016, 2, 2),
        reportDue=datetime(2016, 2, 2),
        reportDoc="N:/FakeLocation/FakeDoc2.pdf"
    ))
    ucr_reports.append(models.UCRReport(
        projectID=3,
        reportTypeID=1,
        reportSubmitted=datetime(2016, 2, 2),
        reportDue=datetime(2016, 2, 2),
        reportDoc="N:/FakeLocation/FakeDoc3.pdf"
    ))
    ucr_reports.append(models.UCRReport(
        projectID=4,
        reportTypeID=1,
        reportSubmitted=datetime(2016, 2, 2),
        reportDue=datetime(2016, 2, 2),
        reportDoc="N:/FakeLocation/FakeDoc4.pdf"
    ))
    ucr_reports.append(models.UCRReport(
        projectID=5,
        reportTypeID=1,
        reportSubmitted=datetime(2016, 2, 2),
        reportDue=datetime(2016, 2, 2),
        reportDoc="N:/FakeLocation/FakeDoc5.pdf"
    ))
    ucr_reports.append(models.UCRReport(
        projectID=1,
        reportTypeID=2,
        reportSubmitted=datetime(2016, 2, 2),
        reportDue=datetime(2016, 2, 2),
        reportDoc="N:/FakeLocation/FakeDoc6.pdf"
    ))
    ucr_reports.append(models.UCRReport(
        projectID=1,
        reportTypeID=2,
        reportSubmitted=datetime(2016, 2, 2),
        reportDue=datetime(2016, 2, 2),
        reportDoc="N:/FakeLocation/FakeDoc7.pdf"
    ))
    ucr_reports.append(models.UCRReport(
        projectID=1,
        reportTypeID=2,
        reportSubmitted=datetime(2016, 2, 2),
        reportDue=datetime(2016, 2, 2),
        reportDoc="N:/FakeLocation/FakeDoc8.pdf"
    ))
    ucr_reports.append(models.UCRReport(
        projectID=1,
        reportTypeID=2,
        reportSubmitted=datetime(2016, 2, 2),
        reportDue=datetime(2016, 2, 2),
        reportDoc="N:/FakeLocation/FakeDoc9.pdf"
    ))
    ucr_reports.append(models.UCRReport(
        projectID=1,
        reportTypeID=2,
        reportSubmitted=datetime(2016, 2, 2),
        reportDue=datetime(2016, 2, 2),
        reportDoc="N:/FakeLocation/FakeDoc10.pdf"
    ))
    return ucr_reports


def create_arc_reviews():
    arcs = []
    arcs.append(
        models.ArcReview(
            projectID=1,
            reviewType=1,
            dateSentToReviewer=datetime(2016, 2, 2),
            reviewer1=1,
            reviewer1Rec=1,
            reviewer1SigDate=datetime(2016, 2, 2),
            reviewer1Comments="test comment",
            reviewer2=2,
            reviewer2Rec=2,
            reviewer2SigDate=datetime(2016, 2, 2),
            reviewer2Comments="test comment",
            research=1,
            linkage=False,
            contact=True,
            engaged=True,
            nonPublicData=True)
    )
    arcs.append(
        models.ArcReview(
            projectID=1,
            reviewType=2,
            dateSentToReviewer=datetime(2016, 2, 2),
            reviewer1=1,
            reviewer1Rec=1,
            reviewer1SigDate=datetime(2016, 2, 2),
            reviewer1Comments="test comment",
            reviewer2=2,
            reviewer2Rec=2,
            reviewer2SigDate=datetime(2016, 2, 2),
            reviewer2Comments="test comment",
            research=1,
            linkage=False,
            contact=True,
            engaged=True,
            nonPublicData=True)
    )
    arcs.append(
        models.ArcReview(
            projectID=2,
            reviewType=1,
            dateSentToReviewer=datetime(2016, 2, 2),
            reviewer1=1,
            reviewer1Rec=1,
            reviewer1SigDate=datetime(2016, 2, 2),
            reviewer1Comments="test comment",
            reviewer2=2,
            reviewer2Rec=2,
            reviewer2SigDate=datetime(2016, 2, 2),
            reviewer2Comments="test comment",
            research=1,
            linkage=False,
            contact=True,
            engaged=True,
            nonPublicData=True)
    )
    arcs.append(
        models.ArcReview(
            projectID=2,
            reviewType=2,
            dateSentToReviewer=datetime(2016, 2, 2),
            reviewer1=1,
            reviewer1Rec=1,
            reviewer1SigDate=datetime(2016, 2, 2),
            reviewer1Comments="test comment",
            reviewer2=2,
            reviewer2Rec=2,
            reviewer2SigDate=datetime(2016, 2, 2),
            reviewer2Comments="test comment",
            research=1,
            linkage=False,
            contact=True,
            engaged=True,
            nonPublicData=True)
    )
    arcs.append(
        models.ArcReview(
            projectID=3,
            reviewType=1,
            dateSentToReviewer=datetime(2016, 2, 2),
            reviewer1=1,
            reviewer1Rec=1,
            reviewer1SigDate=datetime(2016, 2, 2),
            reviewer1Comments="test comment",
            reviewer2=2,
            reviewer2Rec=2,
            reviewer2SigDate=datetime(2016, 2, 2),
            reviewer2Comments="test comment",
            research=1,
            linkage=False,
            contact=True,
            engaged=True,
            nonPublicData=True)
    )
    arcs.append(
        models.ArcReview(
            projectID=3,
            reviewType=2,
            dateSentToReviewer=datetime(2016, 2, 2),
            reviewer1=1,
            reviewer1Rec=1,
            reviewer1SigDate=datetime(2016, 2, 2),
            reviewer1Comments="test comment",
            reviewer2=2,
            reviewer2Rec=2,
            reviewer2SigDate=datetime(2016, 2, 2),
            reviewer2Comments="test comment",
            research=1,
            linkage=False,
            contact=True,
            engaged=True,
            nonPublicData=True)
    )
    arcs.append(
        models.ArcReview(
            projectID=4,
            reviewType=1,
            dateSentToReviewer=datetime(2016, 2, 2),
            reviewer1=1,
            reviewer1Rec=1,
            reviewer1SigDate=datetime(2016, 2, 2),
            reviewer1Comments="test comment",
            reviewer2=2,
            reviewer2Rec=2,
            reviewer2SigDate=datetime(2016, 2, 2),
            reviewer2Comments="test comment",
            research=1,
            linkage=False,
            contact=True,
            engaged=True,
            nonPublicData=True)
    )
    arcs.append(
        models.ArcReview(
            projectID=4,
            reviewType=2,
            dateSentToReviewer=datetime(2016, 2, 2),
            reviewer1=1,
            reviewer1Rec=1,
            reviewer1SigDate=datetime(2016, 2, 2),
            reviewer1Comments="test comment",
            reviewer2=2,
            reviewer2Rec=2,
            reviewer2SigDate=datetime(2016, 2, 2),
            reviewer2Comments="test comment",
            research=1,
            linkage=False,
            contact=True,
            engaged=True,
            nonPublicData=True)
    )
    arcs.append(
        models.ArcReview(
            projectID=5,
            reviewType=1,
            dateSentToReviewer=datetime(2016, 2, 2),
            reviewer1=1,
            reviewer1Rec=1,
            reviewer1SigDate=datetime(2016, 2, 2),
            reviewer1Comments="test comment",
            reviewer2=2,
            reviewer2Rec=2,
            reviewer2SigDate=datetime(2016, 2, 2),
            reviewer2Comments="test comment",
            research=1,
            linkage=False,
            contact=True,
            engaged=True,
            nonPublicData=True)
    )
    arcs.append(
        models.ArcReview(
            projectID=5,
            reviewType=2,
            dateSentToReviewer=datetime(2016, 2, 2),
            reviewer1=1,
            reviewer1Rec=1,
            reviewer1SigDate=datetime(2016, 2, 2),
            reviewer1Comments="test comment",
            reviewer2=2,
            reviewer2Rec=2,
            reviewer2SigDate=datetime(2016, 2, 2),
            reviewer2Comments="test comment",
            research=1,
            linkage=False,
            contact=True,
            engaged=True,
            nonPublicData=True)
    )
    return arcs


def create_fundings():
    fundings = []
    fundings.append(
        models.Funding(
            grantStatusID=1,
            projectID=1,
            fundingSourceID=1,
            primaryFundingSource="pfs",
            secondaryFundingSource="sfs",
            fundingNumber="number",
            grantTitle="title",
            dateStatus=datetime(2016, 2, 2),
            grantPi=1,
            primaryChartfield="pcf",
            secondaryChartfield="scf"
        )
    )
    fundings.append(
        models.Funding(
            grantStatusID=2,
            projectID=1,
            fundingSourceID=2,
            primaryFundingSource="pfs",
            secondaryFundingSource="sfs",
            fundingNumber="number",
            grantTitle="title",
            dateStatus=datetime(2016, 2, 2),
            grantPi=1,
            primaryChartfield="pcf",
            secondaryChartfield="scf"
        )
    )
    fundings.append(
        models.Funding(
            grantStatusID=1,
            projectID=2,
            fundingSourceID=1,
            primaryFundingSource="pfs",
            secondaryFundingSource="sfs",
            fundingNumber="number",
            grantTitle="title",
            dateStatus=datetime(2016, 2, 2),
            grantPi=1,
            primaryChartfield="pcf",
            secondaryChartfield="scf"
        )
    )
    fundings.append(
        models.Funding(
            grantStatusID=2,
            projectID=2,
            fundingSourceID=2,
            primaryFundingSource="pfs",
            secondaryFundingSource="sfs",
            fundingNumber="number",
            grantTitle="title",
            dateStatus=datetime(2016, 2, 2),
            grantPi=1,
            primaryChartfield="pcf",
            secondaryChartfield="scf"
        )
    )
    fundings.append(
        models.Funding(
            grantStatusID=1,
            projectID=3,
            fundingSourceID=1,
            primaryFundingSource="pfs",
            secondaryFundingSource="sfs",
            fundingNumber="number",
            grantTitle="title",
            dateStatus=datetime(2016, 2, 2),
            grantPi=1,
            primaryChartfield="pcf",
            secondaryChartfield="scf"
        )
    )
    fundings.append(
        models.Funding(
            grantStatusID=2,
            projectID=3,
            fundingSourceID=2,
            primaryFundingSource="pfs",
            secondaryFundingSource="sfs",
            fundingNumber="number",
            grantTitle="title",
            dateStatus=datetime(2016, 2, 2),
            grantPi=1,
            primaryChartfield="pcf",
            secondaryChartfield="scf"
        )
    )
    fundings.append(
        models.Funding(
            grantStatusID=1,
            projectID=4,
            fundingSourceID=1,
            primaryFundingSource="pfs",
            secondaryFundingSource="sfs",
            fundingNumber="number",
            grantTitle="title",
            dateStatus=datetime(2016, 2, 2),
            grantPi=1,
            primaryChartfield="pcf",
            secondaryChartfield="scf"
        )
    )
    fundings.append(
        models.Funding(
            grantStatusID=2,
            projectID=4,
            fundingSourceID=2,
            primaryFundingSource="pfs",
            secondaryFundingSource="sfs",
            fundingNumber="number",
            grantTitle="title",
            dateStatus=datetime(2016, 2, 2),
            grantPi=1,
            primaryChartfield="pcf",
            secondaryChartfield="scf"
        )
    )
    fundings.append(
        models.Funding(
            grantStatusID=1,
            projectID=5,
            fundingSourceID=1,
            primaryFundingSource="pfs",
            secondaryFundingSource="sfs",
            fundingNumber="number",
            grantTitle="title",
            dateStatus=datetime(2016, 2, 2),
            grantPi=1,
            primaryChartfield="pcf",
            secondaryChartfield="scf"
        )
    )
    fundings.append(
        models.Funding(
            grantStatusID=2,
            projectID=5,
            fundingSourceID=2,
            primaryFundingSource="pfs",
            secondaryFundingSource="sfs",
            fundingNumber="number",
            grantTitle="title",
            dateStatus=datetime(2016, 2, 2),
            grantPi=1,
            primaryChartfield="pcf",
            secondaryChartfield="scf"
        )
    )
    return fundings


def create_project_statuses2():
    statuses = []
    statuses.append(
        models.ProjectStatus(
            projectStatusTypeID=1,
            projectID=1,
            staffID=1,
            statusDate=datetime(2016, 2, 2),
            statusNotes="notes"
        )
    )
    statuses.append(
        models.ProjectStatus(
            projectStatusTypeID=4,
            projectID=2,
            staffID=1,
            statusDate=datetime(2016, 2, 2),
            statusNotes="notes"
        )
    )
    statuses.append(
        models.ProjectStatus(
            projectStatusTypeID=1,
            projectID=3,
            staffID=1,
            statusDate=datetime(2016, 2, 2),
            statusNotes="notes"
        )
    )
    statuses.append(
        models.ProjectStatus(
            projectStatusTypeID=3,
            projectID=4,
            staffID=1,
            statusDate=datetime(2016, 2, 2),
            statusNotes="notes"
        )
    )
    statuses.append(
        models.ProjectStatus(
            projectStatusTypeID=2,
            projectID=5,
            staffID=1,
            statusDate=datetime(2016, 2, 2),
            statusNotes="notes"
        )
    )
    return statuses


def create_pre_applications():
    preapps = []
    preapps.append(
        models.PreApplication(
            projectID=1,
            piFirstName="pi_fname",
            piLastName="pi_lname",
            piEmail="pi_email",
            piPhone="pi_phone",
            contactFirstName="contact_fname",
            contactLastName="contact_lname",
            contactPhone="contact_phone",
            contactEmail="contact_email",
            institution="institution",
            institution2="institution2",
            uid="uid",
            udoh=1,
            projectTitle="Project 1",
            purpose="purpose",
            irb0=True,
            irb1=True,
            irb2=True,
            irb3=True,
            irb4=True,
            otherIrb="other_irb",
            updb=True,
            ptContact=True,
            startDate=datetime(2016, 2, 2),
            link=True,
            deliveryDate=datetime(2016, 2, 2),
            description="description"
        )
    )
    preapps.append(
        models.PreApplication(
            projectID=2,
            piFirstName="pi_fname",
            piLastName="pi_lname",
            piEmail="pi_email",
            piPhone="pi_phone",
            contactFirstName="contact_fname",
            contactLastName="contact_lname",
            contactPhone="contact_phone",
            contactEmail="contact_email",
            institution="institution",
            institution2="institution2",
            uid="uid",
            udoh=1,
            projectTitle="Project 2",
            purpose="purpose",
            irb0=True,
            irb1=True,
            irb2=True,
            irb3=True,
            irb4=True,
            otherIrb="other_irb",
            updb=True,
            ptContact=True,
            startDate=datetime(2016, 2, 2),
            link=True,
            deliveryDate=datetime(2016, 2, 2),
            description="description"
        )
    )
    preapps.append(
        models.PreApplication(
            projectID=3,
            piFirstName="pi_fname",
            piLastName="pi_lname",
            piEmail="pi_email",
            piPhone="pi_phone",
            contactFirstName="contact_fname",
            contactLastName="contact_lname",
            contactPhone="contact_phone",
            contactEmail="contact_email",
            institution="institution",
            institution2="institution2",
            uid="uid",
            udoh=1,
            projectTitle="Project 3",
            purpose="purpose",
            irb0=True,
            irb1=True,
            irb2=True,
            irb3=True,
            irb4=True,
            otherIrb="other_irb",
            updb=True,
            ptContact=True,
            startDate=datetime(2016, 2, 2),
            link=True,
            deliveryDate=datetime(2016, 2, 2),
            description="description"
        )
    )
    preapps.append(
        models.PreApplication(
            projectID=4,
            piFirstName="pi_fname",
            piLastName="pi_lname",
            piEmail="pi_email",
            piPhone="pi_phone",
            contactFirstName="contact_fname",
            contactLastName="contact_lname",
            contactPhone="contact_phone",
            contactEmail="contact_email",
            institution="institution",
            institution2="institution2",
            uid="uid",
            udoh=1,
            projectTitle="Project 4",
            purpose="purpose",
            irb0=True,
            irb1=True,
            irb2=True,
            irb3=True,
            irb4=True,
            otherIrb="other_irb",
            updb=True,
            ptContact=True,
            startDate=datetime(2016, 2, 2),
            link=True,
            deliveryDate=datetime(2016, 2, 2),
            description="description"
        )
    )
    preapps.append(
        models.PreApplication(
            projectID=5,
            piFirstName="pi_fname",
            piLastName="pi_lname",
            piEmail="pi_email",
            piPhone="pi_phone",
            contactFirstName="contact_fname",
            contactLastName="contact_lname",
            contactPhone="contact_phone",
            contactEmail="contact_email",
            institution="institution",
            institution2="institution2",
            uid="uid",
            udoh=1,
            projectTitle="Project 5",
            purpose="purpose",
            irb0=True,
            irb1=True,
            irb2=True,
            irb3=True,
            irb4=True,
            otherIrb="other_irb",
            updb=True,
            ptContact=True,
            startDate=datetime(2016, 2, 2),
            link=True,
            deliveryDate=datetime(2016, 2, 2),
            description="description"
        )
    )
    return preapps


def create_logs():
    logs = []
    logs.append(
        models.Log(
            logSubjectID=1,
            projectID=1,
            staffID=1,
            phaseStatusID=1,
            note="Test Note 1",
            date=datetime(2016, 2, 2)
        )
    )
    logs.append(
        models.Log(
            logSubjectID=1,
            projectID=2,
            staffID=1,
            phaseStatusID=1,
            note="Test Note 1",
            date=datetime(2016, 2, 2)
        )
    )
    logs.append(
        models.Log(
            logSubjectID=1,
            projectID=3,
            staffID=1,
            phaseStatusID=1,
            note="Test Note 1",
            date=datetime(2016, 2, 2)
        )
    )
    logs.append(
        models.Log(
            logSubjectID=1,
            projectID=4,
            staffID=1,
            phaseStatusID=1,
            note="Test Note 1",
            date=datetime(2016, 2, 2)
        )
    )
    logs.append(
        models.Log(
            logSubjectID=1,
            projectID=5,
            staffID=1,
            phaseStatusID=1,
            note="Test Note 1",
            date=datetime(2016, 2, 2)
        )
    )
    return logs


def create_project_staff():
    project_staff = []
    project_staff.append(models.ProjectStaff(
        staffRoleID=1,
        projectID=1,
        staffID=1,
        datePledge=datetime(2016, 2, 2),
        dateRevoked=datetime(2016, 2, 2),
        contactID=1,
        inactiveID=1
    ))
    project_staff.append(models.ProjectStaff(
        staffRoleID=1,
        projectID=1,
        staffID=2,
        datePledge=datetime(2016, 2, 2),
        dateRevoked=datetime(2016, 2, 2),
        contactID=1,
        inactiveID=1
    ))
    return project_staff


def create_staff_trainings():
    trainings = []
    trainings.append(
        models.StaffTraining(
            staffID=1,
            humanSubjectTrainingID=1,
            dateTaken=datetime(2016, 2, 2),
            dateExpires=datetime(2016, 2, 2)
        )
    )
    trainings.append(
        models.StaffTraining(
            staffID=1,
            humanSubjectTrainingID=2,
            dateTaken=datetime(2016, 2, 2),
            dateExpires=datetime(2016, 2, 2)
        )
    )
    trainings.append(
        models.StaffTraining(
            staffID=2,
            humanSubjectTrainingID=1,
            dateTaken=datetime(2016, 2, 2),
            dateExpires=datetime(2016, 2, 2)
        )
    )
    trainings.append(
        models.StaffTraining(
            staffID=2,
            humanSubjectTrainingID=2,
            dateTaken=datetime(2016, 2, 2),
            dateExpires=datetime(2016, 2, 2)
        )
    )
    return trainings


def create_patients():
    patients = []
    patients.append(models.Patient(
        patID="1",
        ucrDistID=1,
        UPDBID=1,
        firstName="John",
        lastName="Doe",
        middleName="Joe",
        maidenName="",
        aliasFirstName="Johnny",
        aliasLastName="Doey",
        aliasMiddleName="Joey",
        dobDay=15,
        dobMonth=2,
        dobYear=1990,
        SSN="999999999",
        sexID=2,
        raceID=1,
        ethnicityID=1,
        recordNumber='PA-123'
    ))
    patients.append(models.Patient(
        patID="2",
        ucrDistID=1,
        UPDBID=1,
        firstName="John2",
        lastName="Doe2",
        middleName="Joe2",
        maidenName="",
        aliasFirstName="Johnny",
        aliasLastName="Doey",
        aliasMiddleName="Joey",
        dobDay=15,
        dobMonth=2,
        dobYear=1990,
        SSN="999999999",
        sexID=2,
        raceID=1,
        ethnicityID=1,
        recordNumber='PA-313'
            ))
    patients.append(models.Patient(
        patID="3",
        ucrDistID=1,
        UPDBID=1,
        firstName="John3",
        lastName="Doe3",
        middleName="Joe3",
        maidenName="",
        aliasFirstName="Johnny",
        aliasLastName="Doey",
        aliasMiddleName="Joey",
        dobDay=15,
        dobMonth=2,
        dobYear=1990,
        SSN="999999999",
        sexID=2,
        raceID=1,
        ethnicityID=2,
        recordNumber='PA-746'

    ))
    patients.append(models.Patient(
        patID="4",
        ucrDistID=1,
        UPDBID=1,
        firstName="Jane",
        lastName="Doe",
        middleName="Jill",
        maidenName="",
        aliasFirstName="J",
        aliasLastName="Doey",
        aliasMiddleName="Jill",
        dobDay=15,
        dobMonth=2,
        dobYear=1990,
        SSN="999999999",
        sexID=1,
        raceID=3,
        ethnicityID=2,
        recordNumber='PA-567'

    ))
    patients.append(models.Patient(
        patID="4",
        ucrDistID=1,
        UPDBID=1,
        firstName="Jane2",
        lastName="Doe2",
        middleName="Jill2",
        maidenName="",
        aliasFirstName="J",
        aliasLastName="Doey",
        aliasMiddleName="Jill",
        dobDay=15,
        dobMonth=2,
        dobYear=1990,
        SSN="999999999",
        sexID=1,
        raceID=2,
        ethnicityID=2,
        recordNumber='PA-154'
    ))
    return patients


def create_patient_addresses():
    addresses = []
    addresses.append(
        models.PatientAddress(
        contactInfoSourceID=1,
        participantID=1,
        contactInfoStatusID=1,
        street="street",
        street2="street2",
        city="city",
        stateID=1,
        zip="12345",
        addressStatusDate=datetime(2016, 2, 2),
    ))
    addresses.append(
        models.PatientAddress(
        contactInfoSourceID=1,
        participantID=2,
        contactInfoStatusID=1,
        street="street",
        street2="street2",
        city="city",
        stateID=1,
        zip="12345",
        addressStatusDate=datetime(2016, 2, 2),
    ))
    addresses.append(
        models.PatientAddress(
        contactInfoSourceID=1,
        participantID=3,
        contactInfoStatusID=1,
        street="street",
        street2="street2",
        city="city",
        stateID=1,
        zip="12345",
        addressStatusDate=datetime(2016, 2, 2),
    ))
    addresses.append(
        models.PatientAddress(
        contactInfoSourceID=1,
        participantID=4,
        contactInfoStatusID=1,
        street="street",
        street2="street2",
        city="city",
        stateID=1,
        zip="12345",
        addressStatusDate=datetime(2016, 2, 2),
    ))
    addresses.append(
        models.PatientAddress(
        contactInfoSourceID=1,
        participantID=5,
        contactInfoStatusID=1,
        street="street",
        street2="street2",
        city="city",
        stateID=1,
        zip="12345",
        addressStatusDate=datetime(2016, 2, 2),
    ))
    return addresses


def create_patient_emails():
    emails = []
    emails.append(
        models.PatientEmail(
            contactInfoSourceID=1,
            participantID=1,
            contactInfoStatusID=1,
            email="email@gmail.com",
            emailStatusDate=datetime(2016, 2, 2)
        )
    )
    emails.append(
        models.PatientEmail(
            contactInfoSourceID=1,
            participantID=2,
            contactInfoStatusID=1,
            email="email@gmail.com",
            emailStatusDate=datetime(2016, 2, 2)
        )
    )
    emails.append(
        models.PatientEmail(
            contactInfoSourceID=1,
            participantID=3,
            contactInfoStatusID=1,
            email="email@gmail.com",
            emailStatusDate=datetime(2016, 2, 2)
        )
    )
    emails.append(
        models.PatientEmail(
            contactInfoSourceID=1,
            participantID=4,
            contactInfoStatusID=1,
            email="email@gmail.com",
            emailStatusDate=datetime(2016, 2, 2)
        )
    )
    emails.append(
        models.PatientEmail(
            contactInfoSourceID=1,
            participantID=5,
            contactInfoStatusID=1,
            email="email@gmail.com",
            emailStatusDate=datetime(2016, 2, 2)
        )
    )
    return emails


def create_patient_phones():
    phones = []
    phones.append(
        models.PatientPhone(
            contactInfoSourceID=1,
            participantID=1,
            contactInfoStatusID=1,
            phoneTypeID=1,
            phoneNumber="phone",
            phoneStatusDate=datetime(2016, 2, 2)
        )
    )
    phones.append(
        models.PatientPhone(
            contactInfoSourceID=1,
            participantID=2,
            contactInfoStatusID=1,
            phoneTypeID=1,
            phoneNumber="phone",
            phoneStatusDate=datetime(2016, 2, 2)
        )
    )
    phones.append(
        models.PatientPhone(
            contactInfoSourceID=1,
            participantID=3,
            contactInfoStatusID=1,
            phoneTypeID=1,
            phoneNumber="phone",
            phoneStatusDate=datetime(2016, 2, 2)
        )
    )
    phones.append(
        models.PatientPhone(
            contactInfoSourceID=1,
            participantID=4,
            contactInfoStatusID=1,
            phoneTypeID=1,
            phoneNumber="phone",
            phoneStatusDate=datetime(2016, 2, 2)
        )
    )
    phones.append(
        models.PatientPhone(
            contactInfoSourceID=1,
            participantID=5,
            contactInfoStatusID=1,
            phoneTypeID=1,
            phoneNumber="phone",
            phoneStatusDate=datetime(2016, 2, 2)
        )
    )
    return phones


def create_informants():
    informants = []
    informants.append(models.Informant(
        participantID=1,
        firstName="Joe",
        lastName="Smith",
        middleName="",
        informantPrimary=True,
        informantRelationshipID=1,
        notes="notes"
    ))
    informants.append(models.Informant(
        participantID=2,
        firstName="Joe2",
        lastName="Smith2",
        middleName="",
        informantPrimary=True,
        informantRelationshipID=6,
        notes="notes"
    ))
    informants.append(models.Informant(
        participantID=3,
        firstName="Joe3",
        lastName="Smith3",
        middleName="",
        informantPrimary=True,
        informantRelationshipID=12,
        notes="notes"
    ))
    informants.append(models.Informant(
        participantID=4,
        firstName="Joe4",
        lastName="Smith4",
        middleName="",
        informantPrimary=True,
        informantRelationshipID=14,
        notes="notes"
    ))
    informants.append(models.Informant(
        participantID=5,
        firstName="Joe5",
        lastName="Smith5",
        middleName="",
        informantPrimary=True,
        informantRelationshipID=20,
        notes="notes"
    ))
    return informants


def create_informant_addresses():
    informant_addresses = []
    informant_addresses.append(models.InformantAddress(
        contactInfoSourceID=1,
        informantID=1,
        contactInfoStatusID=1,
        street="street",
        street2="street2",
        city="city",
        stateID=2,
        zip="12345",
        addressStatusDate=datetime(2016, 2, 2),
    ))
    informant_addresses.append(models.InformantAddress(
        contactInfoSourceID=1,
        informantID=2,
        contactInfoStatusID=1,
        street="street",
        street2="street2",
        city="city",
        stateID=2,
        zip="12345",
        addressStatusDate=datetime(2016, 2, 2),
    ))
    informant_addresses.append(models.InformantAddress(
        contactInfoSourceID=1,
        informantID=3,
        contactInfoStatusID=1,
        street="street",
        street2="street2",
        city="city",
        stateID=2,
        zip="12345",
        addressStatusDate=datetime(2016, 2, 2),
    ))
    informant_addresses.append(models.InformantAddress(
        contactInfoSourceID=1,
        informantID=4,
        contactInfoStatusID=1,
        street="street",
        street2="street2",
        city="city",
        stateID=2,
        zip="12345",
        addressStatusDate=datetime(2016, 2, 2),
    ))
    informant_addresses.append(models.InformantAddress(
        contactInfoSourceID=1,
        informantID=5,
        contactInfoStatusID=1,
        street="street",
        street2="street2",
        city="city",
        stateID=2,
        zip="12345",
        addressStatusDate=datetime(2016, 2, 2),
    ))
    return informant_addresses


def create_informant_phones():
    informant_phones = []
    informant_phones.append(models.InformantPhone(
        contactInfoSourceID=1,
        informantID=1,
        contactInfoStatusID=1,
        phoneTypeID=1,
        phoneNumber="123-456-999 ext 1",
        phoneStatusDate=datetime(2016, 2, 2)
    ))
    informant_phones.append(models.InformantPhone(
        contactInfoSourceID=1,
        informantID=2,
        contactInfoStatusID=1,
        phoneTypeID=1,
        phoneNumber="123-456-999 ext 2",
        phoneStatusDate=datetime(2016, 2, 2)
    ))
    informant_phones.append(models.InformantPhone(
        contactInfoSourceID=1,
        informantID=3,
        contactInfoStatusID=1,
        phoneTypeID=1,
        phoneNumber="123-456-999 ext 3",
        phoneStatusDate=datetime(2016, 2, 2)
    ))
    informant_phones.append(models.InformantPhone(
        contactInfoSourceID=1,
        informantID=4,
        contactInfoStatusID=1,
        phoneTypeID=1,
        phoneNumber="123-456-999 ext 4",
        phoneStatusDate=datetime(2016, 2, 2)
    ))
    informant_phones.append(models.InformantPhone(
        contactInfoSourceID=1,
        informantID=5,
        contactInfoStatusID=1,
        phoneTypeID=1,
        phoneNumber="123-456-999 ext 5",
        phoneStatusDate=datetime(2016, 2, 2)
    ))
    return informant_phones


def create_ctcs():
    ctcs = []
    ctcs.append(models.CTC(
        participantID=1,
        dxDateDay=2,
        dxDateMonth=7,
        dxDateYear=1998,
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
        recordID="1",
        ctcRecordNumber='ctc-234',
        dmsCtcID=345

    ))
    ctcs.append(models.CTC(
        participantID=2,
        dxDateDay=2,
        dxDateMonth=7,
        dxDateYear=1998,
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
        recordID="2",
        ctcRecordNumber='ctc-874',
        dmsCtcID=9876
    ))
    ctcs.append(models.CTC(
        participantID=3,
        dxDateDay=2,
        dxDateMonth=7,
        dxDateYear=1998,
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
        recordID="3",
        ctcRecordNumber='ctc-984',
        dmsCtcID=6765
    ))
    ctcs.append(models.CTC(
        participantID=4,
        dxDateDay=2,
        dxDateMonth=7,
        dxDateYear=1998,
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
        recordID="4",
        ctcRecordNumber='ctc-4',
        dmsCtcID=2111
    ))
    ctcs.append(models.CTC(
        participantID=5,
        dxDateDay=2,
        dxDateMonth=7,
        dxDateYear=1998,
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
        recordID="5",
        ctcRecordNumber='ctc-56',
        dmsCtcID=980
    ))
    return ctcs


def create_project_patients():
    pps = []
    pps.append(
        models.ProjectPatient(
            projectID=1,
            staffID=1,
            ctcID=1,
            currentAge=1,
            batch=1,
            siteGrpID=1,
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
            vitalStatusID=4,
            monthOfLastConsent=1,
            yearOfLastConsent=2016
        )
    )
    pps.append(
        models.ProjectPatient(
            projectID=2,
            staffID=1,
            ctcID=2,
            currentAge=1,
            batch=1,
            siteGrpID=1,
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
            vitalStatusID=4,
            dayOfLastConsent=5,

            yearOfLastConsent=2016
        )
    )
    pps.append(
        models.ProjectPatient(
            projectID=3,
            staffID=1,
            ctcID=3,
            currentAge=1,
            batch=1,
            siteGrpID=1,
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
            vitalStatusID=4,
            dayOfLastConsent=4,
            monthOfLastConsent=3,
            yearOfLastConsent=2014
        )
    )
    pps.append(
        models.ProjectPatient(
            projectID=4,
            staffID=1,
            ctcID=4,
            currentAge=1,
            batch=1,
            siteGrpID=1,
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
            vitalStatusID=1,
            dayOfLastConsent=28,
            monthOfLastConsent=9,
            yearOfLastConsent=2015
        )
    )
    pps.append(
        models.ProjectPatient(
            projectID=5,
            staffID=1,
            ctcID=5,
            currentAge=1,
            batch=1,
            siteGrpID=1,
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
            vitalStatusID=1,
            monthOfLastConsent=12,
            yearOfLastConsent=2012
        )
    )
    return pps

def create_project_sitegroups():
    project_sites = []
    project_sites.append(models.ProjectSiteGroups(
        projectID=1,
        siteGroupID=1,
        siteGroupDate= datetime(2016, 2, 2)
    ))
    project_sites.append(models.ProjectSiteGroups(
        projectID=2,
        siteGroupID=2,
        siteGroupDate=datetime(2016, 1, 2)
    ))
    project_sites.append(models.ProjectSiteGroups(
        projectID=3,
        siteGroupID=1,
        siteGroupDate=datetime(2015, 2, 2)
    ))
    project_sites.append(models.ProjectSiteGroups(
        projectID=3,
        siteGroupID=3,
        siteGroupDate=datetime(2014, 12, 2)
    ))
    return project_sites

def create_tracings():
    tracings = []
    tracings.append(models.Tracing(
        tracingSourceID=1,
        participantID=1,
        date=datetime(2016, 2, 2),
        staffID=1,
        notes="notes"
    ))
    tracings.append(models.Tracing(
        tracingSourceID=1,
        participantID=2,
        date=datetime(2016, 2, 2),
        staffID=1,
        notes="notes"
    ))
    tracings.append(models.Tracing(
        tracingSourceID=1,
        participantID=3,
        date=datetime(2016, 2, 2),
        staffID=1,
        notes="notes"
    ))
    tracings.append(models.Tracing(
        tracingSourceID=1,
        participantID=4,
        date=datetime(2016, 2, 2),
        staffID=1,
        notes="notes"
    ))
    tracings.append(models.Tracing(
        tracingSourceID=1,
        participantID=5,
        date=datetime(2016, 2, 2),
        staffID=1,
        notes="notes"
    ))
    return tracings


def create_physicians():
    physicians = []
    physicians.append(
        models.Physician(
            firstName="Bill",
            lastName="Walden",
            middleName="",
            credentials="MD",
            specialty="specialty",
            aliasFirstName="alias_fname",
            aliasLastName="alias_lname",
            aliasMiddleName="alias_middle_name",
            physicianStatusID=1,
            physicianStatusDate=datetime(2016, 2, 2),
            displayID='DP-548'
        )
    )
    physicians.append(
        models.Physician(
            firstName="Bob",
            lastName="Smith",
            middleName="",
            credentials="MD",
            specialty="specialty",
            aliasFirstName="alias_fname",
            aliasLastName="alias_lname",
            aliasMiddleName="alias_middle_name",
            physicianStatusID=1,
            physicianStatusDate=datetime(2016, 2, 2),
            displayID='DP-363'
        )
    )
    physicians.append(
        models.Physician(
            firstName="Jill",
            lastName="Walden",
            middleName="",
            credentials="MD",
            specialty="specialty",
            aliasFirstName="alias_fname",
            aliasLastName="alias_lname",
            aliasMiddleName="alias_middle_name",
            physicianStatusID=1,
            physicianStatusDate=datetime(2016, 2, 2),
            displayID='DP-4836'
        )
    )
    return physicians


def create_physician_addresses():
    addresses = []
    addresses.append(models.PhysicianAddress(
        contactInfoSourceID=2,
        physicianID=1,
        contactInfoStatusID=2,
        street="street",
        street2="street2",
        city="city",
        stateID=1,
        zip="12345",
        addressStatusDate=datetime(2016, 2, 2),
    ))
    addresses.append(models.PhysicianAddress(
        contactInfoSourceID=2,
        physicianID=2,
        contactInfoStatusID=2,
        street="street",
        street2="street2",
        city="city",
        stateID=1,
        zip="12345",
        addressStatusDate=datetime(2016, 2, 2),
    ))
    addresses.append(models.PhysicianAddress(
        contactInfoSourceID=2,
        physicianID=3,
        contactInfoStatusID=2,
        street="street",
        street2="street2",
        city="city",
        stateID=1,
        zip="12345",
        addressStatusDate=datetime(2016, 2, 2),
    ))
    return addresses


def create_physician_emails():
    emails = []
    emails.append(
        models.PhysicianEmail(
            contactInfoSourceID=1,
            physicianID=1,
            contactInfoStatusID=1,
            email="email@gmail.com",
            emailStatusDate=datetime(2016, 2, 2)
        )
    )
    emails.append(
        models.PhysicianEmail(
            contactInfoSourceID=1,
            physicianID=2,
            contactInfoStatusID=1,
            email="email@gmail.com",
            emailStatusDate=datetime(2016, 2, 2)
        )
    )
    emails.append(
        models.PhysicianEmail(
            contactInfoSourceID=1,
            physicianID=3,
            contactInfoStatusID=1,
            email="email@gmail.com",
            emailStatusDate=datetime(2016, 2, 2)
        )
    )
    return emails


def create_physician_phones():
    phones = []
    phones.append(
        models.PhysicianPhone(
            contactInfoSourceID=1,
            physicianID=1,
            contactInfoStatusID=1,
            phoneNumber="999-999-999",
            phoneTypeID=1,
            phoneStatusDate=datetime(2016, 2, 2)
        )
    )
    phones.append(
        models.PhysicianPhone(
            contactInfoSourceID=1,
            physicianID=2,
            contactInfoStatusID=1,
            phoneNumber="999-999-999",
            phoneTypeID=1,
            phoneStatusDate=datetime(2016, 2, 2)
        )
    )
    phones.append(
        models.PhysicianPhone(
            contactInfoSourceID=1,
            physicianID=2,
            contactInfoStatusID=1,
            phoneNumber="999-999-999",
            phoneTypeID=1,
            phoneStatusDate=datetime(2016, 2, 2)
        )
    )
    return phones


def create_physician_to_ctcs():
    ptcs = []
    ptcs.append(
        models.PhysicianToCTC(
            physicianID=1,
            ctcID=1
        )
    )
    ptcs.append(
        models.PhysicianToCTC(
            physicianID=2,
            ctcID=2
        )
    )
    ptcs.append(
        models.PhysicianToCTC(
            physicianID=3,
            ctcID=3
        )
    )
    ptcs.append(
        models.PhysicianToCTC(
            physicianID=1,
            ctcID=4
        )
    )
    ptcs.append(
        models.PhysicianToCTC(
            physicianID=1,
            ctcID=5
        )
    )
    return ptcs


def create_facilities():
    facilities = []
    facilities.append(models.Facility(
        facilityName="Facility 1",
        contactFirstName="fname",
        contactLastName="lname",
        facilityStatus=1,
        facilityStatusDate=datetime(2016, 2, 2),
        contact2FirstName="fname",
        contact2LastName="lname",
        displayID='FDP-484'
    ))
    facilities.append(models.Facility(
        facilityName="Facility 2",
        contactFirstName="fname",
        contactLastName="lname",
        facilityStatus=1,
        facilityStatusDate=datetime(2016, 2, 2),
        contact2FirstName="fname",
        contact2LastName="lname",
        displayID='FDP-787'
    ))
    return facilities


def create_faciliy_addresses():
    addresses = []
    addresses.append(models.FacilityAddress(
        contactInfoSourceID=1,
        facilityID=1,
        contactInfoStatusID=1,
        street="street",
        street2="street2",
        city="city",
        stateID=1,
        zip="12345",
        addressStatusDate=datetime(2016, 2, 2),
    ))
    addresses.append(models.FacilityAddress(
        contactInfoSourceID=1,
        facilityID=2,
        contactInfoStatusID=1,
        street="street",
        street2="street2",
        city="city",
        stateID=1,
        zip="12345",
        addressStatusDate=datetime(2016, 2, 2),
    ))
    return addresses


def create_facility_phones():
    phones = []
    phones.append(models.FacilityPhone(
        contactInfoSourceID=1,
        facilityID=1,
        contactInfoStatusID=1,
        clinicName="clinic",
        phoneTypeID=1,
        phoneNumber="phone",
        phoneStatusDate=datetime(2016, 2, 2)
    ))
    phones.append(models.FacilityPhone(
        contactInfoSourceID=1,
        facilityID=2,
        contactInfoStatusID=1,
        clinicName="clinic",
        phoneTypeID=1,
        phoneNumber="phone",
        phoneStatusDate=datetime(2016, 2, 2)
    ))
    return phones


def create_patient_project_status_types():
    status_types = []
    status_types.append(models.PatientProjectStatusLUT(
        statusDescription="Status 1",
        patientProjectStatusTypeID=1
    ))
    status_types.append(models.PatientProjectStatusLUT(
        statusDescription="Status 2",
        patientProjectStatusTypeID=2
    ))
    status_types.append(models.PatientProjectStatusLUT(
        statusDescription="Status 3",
        patientProjectStatusTypeID=3
    ))
    return status_types


def create_patient_project_statuses():
    statuses = []
    statuses.append(
        models.PatientProjectStatus(
            patientProjectStatusTypeID=1,
            participantID=1,
            statusDate = datetime(2016,8,9),
            staffID=1
        )
    )
    statuses.append(
        models.PatientProjectStatus(
            patientProjectStatusTypeID=1,
            participantID=2,
            statusDate=datetime(2016, 8, 9),
            staffID=4
        )
    )
    statuses.append(
        models.PatientProjectStatus(
            patientProjectStatusTypeID=1,
            participantID=3,
            statusDate=datetime(2016, 8, 9),
            staffID=5
        )
    )
    statuses.append(
        models.PatientProjectStatus(
            patientProjectStatusTypeID=1,
            participantID=4,
            statusDate=datetime(2016, 8, 9),
            staffID=3
        )
    )
    statuses.append(
        models.PatientProjectStatus(
            patientProjectStatusTypeID=1,
            participantID=5,
            statusDate=datetime(2016, 8, 9),
            staffID=7
        )
    )
    return statuses


def create_physician_facilities():
    pfs = []
    pfs.append(
        models.PhysicianFacility(
            facilityID=1,
            physicianID=1,
            physFacilityStatusID=1,
            physFacilityStatusDate=datetime(2016, 2, 2)
        )
    )
    pfs.append(
        models.PhysicianFacility(
            facilityID=2,
            physicianID=2,
            physFacilityStatusID=1,
            physFacilityStatusDate=datetime(2016, 2, 2)
        )
    )
    pfs.append(
        models.PhysicianFacility(
            facilityID=2,
            physicianID=3,
            physFacilityStatusID=1,
            physFacilityStatusDate=datetime(2016, 2, 2)
        )
    )
    return pfs


def create_ctc_to_facilities():
    cfs = []
    cfs.append(
        models.CTCFacility(
            ctcID=1,
            facilityID=1,
            coc=123
        )
    )
    cfs.append(
        models.CTCFacility(
            ctcID=2,
            facilityID=2,
            coc=123
        )
    )
    cfs.append(
        models.CTCFacility(
            ctcID=3,
            facilityID=2,
            coc=123
        )
    )
    cfs.append(
        models.CTCFacility(
            ctcID=4,
            facilityID=1,
            coc=123
        )
    )
    cfs.append(
        models.CTCFacility(
            ctcID=5,
            facilityID=2,
            coc=123
        )
    )
    return cfs


def create_pp_contacts():
    contacts = []
    for i in range(1,6):
        contacts.append(
            models.Contact(
                contactTypeLUTID=1,
                participantID=i,
                staffID=1,
                informantID=1,
                informantPhoneID=1,
                description="desc",
                contactDate=datetime(2016, 2, 2),
                initials="atp",
                notes="notes"
        ))
        contacts.append(models.Contact(
            contactTypeLUTID=2,
            participantID=i,
            staffID=1,
            facilityID=1,
            facilityPhoneID=1,
            description="desc",
            contactDate=datetime(2016, 2, 2),
            initials="atp",
            notes="notes"
        ))
        contacts.append(models.Contact(
            contactTypeLUTID=3,
            participantID=i,
            staffID=1,
            physicianID=1,
            physicianPhoneID=1,
            description="desc",
            contactDate=datetime(2016, 2, 2),
            initials="atp",
            notes="notes"
        ))
        contacts.append(models.Contact(
            contactTypeLUTID=4,
            participantID=i,
            staffID=1,
            patientPhoneID=1,
            description="desc",
            contactDate=datetime(2016, 2, 2),
            initials="atp",
            notes="notes"
        ))
    return contacts


def create_incentives():
    incentives = []
    incentives.append(
        models.Incentive(
            participantID=1,
            incentiveDescription="desc",
            barcode="123456789",
            dateGiven=datetime(2016, 4, 3)
        )
    )
    incentives.append(
        models.Incentive(
            participantID=2,
            incentiveDescription="desc",
            barcode="123456788",
            dateGiven=datetime(2016, 4, 3)
        )
    )
    incentives.append(
        models.Incentive(
            participantID=3,
            incentiveDescription="desc",
            barcode="123456787",
            dateGiven=datetime(2016, 4, 3)
        )
    )
    incentives.append(
        models.Incentive(
            participantID=4,
            incentiveDescription="desc",
            barcode="123456786",
            dateGiven=datetime(2016, 4, 3)
        )
    )
    incentives.append(
        models.Incentive(
            participantID=5,
            incentiveDescription="desc",
            barcode="123456785",
            dateGiven=datetime(2016, 4, 3)
        )
    )
    return incentives


def populate_db():
    """
    This creates the database/tables and populates it with junk data for testing
    :return:
    """
    db.drop_all()
    db.create_all()

    ucrRoles = create_ucr_roles()
    informantRelationships = create_informant_relationships()
    users = create_users()
    finalCodes = create_final_codes()
    states = create_states()
    abstractStatuses = create_abstract_statuses()
    sexes = create_sexes()
    races = create_races()
    ethnicities = create_ethnicities()
    vitals = create_vital_statuses()
    contacts = create_contacts()
    inactives = create_inactives()
    ucrReportTypes = create_ucr_report_types()
    physicianStatuses = create_physician_statuses()
    physFacilityStatuses = create_physician_facility_statuses()
    phoneTypes = create_phone_types()
    irbHolders = create_irb_holders()
    projectTypes = create_project_types()
    contactStatuses = create_contact_statuses()
    contactSources = create_contact_sources()
    grantStatuses = create_grant_statuses()
    fundingSources = create_funding_sources()
    reviewCommitteeStatuses = create_review_committee_statuses()
    projectStatuses = create_project_statuses()
    logTypes = create_log_subjects()
    reviewCommittees = create_review_committees()
    staffRoles = create_staff_roles()
    projectPhases = create_project_phases()
    hsts = create_human_subject_trainings()
    tracingSources = create_tracing_sources()
    contactTypes = create_contact_types()
    giftCards = create_gift_cards()
    siteGroups= create_sitegroup()
    projectSiteGroups=create_project_sitegroups()

    projects = create_projects()
    budgets = create_budgets()
    projectReviewCommittees = create_project_review_committees()
    ucr_reports = create_ucr_reports()
    arc_reviews = create_arc_reviews()
    fundings = create_fundings()
    staff = create_staff()
    proj_statuses = create_project_statuses2()
    pre_applications = create_pre_applications()
    logs = create_logs()
    project_staff = create_project_staff()
    staff_trainings = create_staff_trainings()
    patients = create_patients()
    patient_addresses = create_patient_addresses()
    patient_emails = create_patient_emails()
    patient_phones = create_patient_phones()
    informants = create_informants()
    informant_addresses = create_informant_addresses()
    informant_phones = create_informant_phones()
    ctcs = create_ctcs()
    project_patients = create_project_patients()
    tracings = create_tracings()
    physicians = create_physicians()
    physician_addresses = create_physician_addresses()
    physician_emails = create_physician_emails()
    physician_phones = create_physician_phones()
    physician_to_ctcs = create_physician_to_ctcs()
    facilities = create_facilities()
    facility_addresses = create_faciliy_addresses()
    facility_phones = create_facility_phones()
    patient_project_status_types = create_patient_project_status_types()
    patient_project_statuses = create_patient_project_statuses()
    physician_facilities = create_physician_facilities()
    ctc_to_facilities = create_ctc_to_facilities()
    pp_contacts = create_pp_contacts()
    incentives = create_incentives()

    # Basic things to get started
    db.session.add_all(ucrRoles)
    db.session.add_all(users)
    db.session.add_all(states)
    db.session.add_all(staff)

	# Basic LUTS to initialize app
    db.session.add_all(sexes)
    db.session.add_all(ethnicities)
    db.session.add_all(races)
    db.session.add_all(informantRelationships)
    db.session.add_all(vitals)
    db.session.add_all(contacts)
    db.session.add_all(inactives)

    # Mostly LUTS
    db.session.add_all(finalCodes)
    db.session.add_all(staffRoles)
    db.session.add_all(abstractStatuses)
    db.session.add_all(contacts)
    db.session.add_all(inactives)
    db.session.add_all(ucrReportTypes)
    db.session.add_all(physicianStatuses)
    db.session.add_all(physFacilityStatuses)
    db.session.add_all(phoneTypes)
    db.session.add_all(irbHolders)
    db.session.add_all(projectTypes)
    db.session.add_all(contactStatuses)
    db.session.add_all(contactSources)
    db.session.add_all(grantStatuses)
    db.session.add_all(fundingSources)
    db.session.add_all(reviewCommitteeStatuses)
    db.session.add_all(projectStatuses)
    db.session.add_all(logTypes)
    db.session.add_all(reviewCommittees)
    db.session.add_all(projectPhases)
    db.session.add_all(hsts)
    db.session.add_all(tracingSources)
    db.session.add_all(contactTypes)
    db.session.add_all(giftCards)
    db.session.add_all(siteGroups)
    db.session.add_all(projectSiteGroups)

    # Main Tables
    db.session.add_all(projects)
    db.session.add_all(budgets)
    db.session.add_all(projectReviewCommittees)
    db.session.add_all(ucr_reports)
    db.session.add_all(arc_reviews)
    db.session.add_all(fundings)
    db.session.add_all(proj_statuses)
    db.session.add_all(pre_applications)
    db.session.add_all(logs)
    db.session.add_all(project_staff)
    db.session.add_all(staff_trainings)
    db.session.add_all(patients)
    db.session.add_all(patient_addresses)
    db.session.add_all(patient_emails)
    db.session.add_all(patient_phones)
    db.session.add_all(informants)
    db.session.add_all(informant_addresses)
    db.session.add_all(informant_phones)
    db.session.add_all(ctcs)
    db.session.add_all(project_patients)
    db.session.add_all(tracings)
    db.session.add_all(physicians)
    db.session.add_all(physician_addresses)
    db.session.add_all(physician_emails)
    db.session.add_all(physician_phones)
    db.session.add_all(physician_to_ctcs)
    db.session.add_all(facilities)
    db.session.add_all(facility_addresses)
    db.session.add_all(facility_phones)
    db.session.add_all(patient_project_status_types)
    db.session.add_all(patient_project_statuses)
    db.session.add_all(physician_facilities)
    db.session.add_all(ctc_to_facilities)
    db.session.add_all(pp_contacts)
    db.session.add_all(incentives)
    db.session.commit()


def create_app(config):
    app = Flask(__name__)
    app.config.from_pyfile(config)
    db.init_app(app)
    return app

if __name__ == "__main__":
    app = create_app("config.py").app_context().push()
    populate_db()
    print("Seeded Database")