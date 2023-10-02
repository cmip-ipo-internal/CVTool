structure = ['required_global_attributes',
 'version_metadata',
 'license',
 'activity_id',
 'institution_id',
 'source_id',
 'source_type',
 'frequency',
 'grid_label',
 'nominal_resolution',
 'realm',
 'table_id',
 'DRS',
 'mip_era',
 'sub_experiment_id',
 'experiment_id',
 'product',
 'tracking_id',
 'further_info_url',
 'realization_index',
 'variant_label',
 'data_specs_version',
 'Conventions',
 'forcing_index',
 'initialization_index',
 'physics_index']

structure.sort()



source_type =  {
            "AER":"aerosol treatment in an atmospheric model where concentrations are calculated based on emissions, transformation, and removal processes (rather than being prescribed or omitted entirely)",
            "AGCM":"atmospheric general circulation model run with prescribed ocean surface conditions and usually a model of the land surface",
            "AOGCM":"coupled atmosphere-ocean global climate model, additionally including explicit representation of at least the land and sea ice",
            "BGC":"biogeochemistry model component that at the very least accounts for carbon reservoirs and fluxes in the atmosphere, terrestrial biosphere, and ocean",
            "CHEM":"chemistry treatment in an atmospheric model that calculates atmospheric oxidant concentrations (including at least ozone), rather than prescribing them",
            "ISM":"ice-sheet model that includes ice-flow",
            "LAND":"land model run uncoupled from the atmosphere",
            "OGCM":"ocean general circulation model run uncoupled from an AGCM but, usually including a sea-ice model",
            "RAD":"radiation component of an atmospheric model run 'offline'",
            "SLAB":"slab-ocean used with an AGCM in representing the atmosphere-ocean coupled system"
        }


frequency = {
            "1hr":"sampled hourly",
            "1hrCM":"monthly-mean diurnal cycle resolving each day into 1-hour means",
            "1hrPt":"sampled hourly, at specified time point within an hour",
            "3hr":"3 hourly mean samples",
            "3hrPt":"sampled 3 hourly, at specified time point within the time period",
            "6hr":"6 hourly mean samples",
            "6hrPt":"sampled 6 hourly, at specified time point within the time period",
            "day":"daily mean samples",
            "dec":"decadal mean samples",
            "fx":"fixed (time invariant) field",
            "mon":"monthly mean samples",
            "monC":"monthly climatology computed from monthly mean samples",
            "monPt":"sampled monthly, at specified time point within the time period",
            "subhrPt":"sampled sub-hourly, at specified time point within an hour",
            "yr":"annual mean samples",
            "yrPt":"sampled yearly, at specified time point within the time period"
        }

frequencykeys = list(frequency.keys())
frequencypattern = "|".join(frequencykeys)


template = {"product":[
            "model-output"
        ],
        "tracking_id":[
            "hdl:21.14100/.*"
        ],

        "realization_index":[
            "^\\[\\{0,\\}[[:digit:]]\\{1,\\}\\]\\{0,\\}$"
        ],
        "variant_label":[
            "r[[:digit:]]\\{1,\\}i[[:digit:]]\\{1,\\}p[[:digit:]]\\{1,\\}f[[:digit:]]\\{1,\\}$"
        ],
        "data_specs_version":[
            "^[[:digit:]]\\{1,2\\}\\.[[:digit:]]\\{1,2\\}\\.[[:digit:]]\\{1,3\\}\\.[[:digit:]]\\{1,3\\}$"
        ],
        "Conventions":[
            "^CF-1.7 CMIP-6.[0-3]\\( UGRID-1.0\\)\\{0,\\}$"
        ],
        "forcing_index":[
            "^\\[\\{0,\\}[[:digit:]]\\{1,\\}\\]\\{0,\\}$"
        ],
        "initialization_index":[
            "^\\[\\{0,\\}[[:digit:]]\\{1,\\}\\]\\{0,\\}$"
        ],
        "physics_index":[
            "^\\[\\{0,\\}[[:digit:]]\\{1,\\}\\]\\{0,\\}$"
        ],
        
        "frequency":frequency,
        "grid_label":{
            "gm":"global mean data",
            "gn":"data reported on a model's native grid",
            "gna":"data reported on a native grid in the region of Antarctica",
            "gng":"data reported on a native grid in the region of Greenland",
            "gnz":"zonal mean data reported on a model's native latitude grid",
            "gr":"regridded data reported on the data provider's preferred target grid",
            "gr1":"regridded data reported on a grid other than the native grid and other than the preferred target grid",
            "gr1a":"regridded data reported in the region of Antarctica on a grid other than the native grid and other than the preferred target grid",
            "gr1g":"regridded data reported in the region of Greenland on a grid other than the native grid and other than the preferred target grid",
            "gr1z":"regridded zonal mean data reported on a grid other than the native latitude grid and other than the preferred latitude target grid",
            "gr2":"regridded data reported on a grid other than the native grid and other than the preferred target grid",
            "gr2a":"regridded data reported in the region of Antarctica on a grid other than the native grid and other than the preferred target grid",
            "gr2g":"regridded data reported in the region of Greenland on a grid other than the native grid and other than the preferred target grid",
            "gr2z":"regridded zonal mean data reported on a grid other than the native latitude grid and other than the preferred latitude target grid",
            "gr3":"regridded data reported on a grid other than the native grid and other than the preferred target grid",
            "gr3a":"regridded data reported in the region of Antarctica on a grid other than the native grid and other than the preferred target grid",
            "gr3g":"regridded data reported in the region of Greenland on a grid other than the native grid and other than the preferred target grid",
            "gr3z":"regridded zonal mean data reported on a grid other than the native latitude grid and other than the preferred latitude target grid",
            "gr4":"regridded data reported on a grid other than the native grid and other than the preferred target grid",
            "gr4a":"regridded data reported in the region of Antarctica on a grid other than the native grid and other than the preferred target grid",
            "gr4g":"regridded data reported in the region of Greenland on a grid other than the native grid and other than the preferred target grid",
            "gr4z":"regridded zonal mean data reported on a grid other than the native latitude grid and other than the preferred latitude target grid",
            "gr5":"regridded data reported on a grid other than the native grid and other than the preferred target grid",
            "gr5a":"regridded data reported in the region of Antarctica on a grid other than the native grid and other than the preferred target grid",
            "gr5g":"regridded data reported in the region of Greenland on a grid other than the native grid and other than the preferred target grid",
            "gr5z":"regridded zonal mean data reported on a grid other than the native latitude grid and other than the preferred latitude target grid",
            "gr6":"regridded data reported on a grid other than the native grid and other than the preferred target grid",
            "gr6a":"regridded data reported in the region of Antarctica on a grid other than the native grid and other than the preferred target grid",
            "gr6g":"regridded data reported in the region of Greenland on a grid other than the native grid and other than the preferred target grid",
            "gr6z":"regridded zonal mean data reported on a grid other than the native latitude grid and other than the preferred latitude target grid",
            "gr7":"regridded data reported on a grid other than the native grid and other than the preferred target grid",
            "gr7a":"regridded data reported in the region of Antarctica on a grid other than the native grid and other than the preferred target grid",
            "gr7g":"regridded data reported in the region of Greenland on a grid other than the native grid and other than the preferred target grid",
            "gr7z":"regridded zonal mean data reported on a grid other than the native latitude grid and other than the preferred latitude target grid",
            "gr8":"regridded data reported on a grid other than the native grid and other than the preferred target grid",
            "gr8a":"regridded data reported in the region of Antarctica on a grid other than the native grid and other than the preferred target grid",
            "gr8g":"regridded data reported in the region of Greenland on a grid other than the native grid and other than the preferred target grid",
            "gr8z":"regridded zonal mean data reported on a grid other than the native latitude grid and other than the preferred latitude target grid",
            "gr9":"regridded data reported on a grid other than the native grid and other than the preferred target grid",
            "gr9a":"regridded data reported in the region of Antarctica on a grid other than the native grid and other than the preferred target grid",
            "gr9g":"regridded data reported in the region of Greenland on a grid other than the native grid and other than the preferred target grid",
            "gr9z":"regridded zonal mean data reported on a grid other than the native latitude grid and other than the preferred latitude target grid",
            "gra":"regridded data in the region of Antarctica reported on the data provider's preferred target grid",
            "grg":"regridded data in the region of Greenland reported on the data provider's preferred target grid",
            "grz":"regridded zonal mean data reported on the data provider's preferred latitude target grid"
        },
        "nominal_resolution":[
            "0.5 km",
            "1 km",
            "10 km",
            "100 km",
            "1000 km",
            "10000 km",
            "1x1 degree",
            "2.5 km",
            "25 km",
            "250 km",
            "2500 km",
            "5 km",
            "50 km",
            "500 km",
            "5000 km"
        ],
        "realm":{
            "aerosol":"Aerosol",
            "atmos":"Atmosphere",
            "atmosChem":"Atmospheric Chemistry",
            "land":"Land Surface",
            "landIce":"Land Ice",
            "ocean":"Ocean",
            "ocnBgchem":"Ocean Biogeochemistry",
            "seaIce":"Sea Ice"
        },

        "version_metadata":{
            "CV_collection_version":"0.0.1"
        }
        
        }

'''

institutions = {
        "AER":"Research and Climate Group, Atmospheric and Environmental Research, 131 Hartwell Avenue, Lexington, MA 02421, USA",
        "AS-RCEC":"Research Center for Environmental Changes, Academia Sinica, Nankang, Taipei 11529, Taiwan",
        "AWI":"Alfred Wegener Institute, Helmholtz Centre for Polar and Marine Research, Am Handelshafen 12, 27570 Bremerhaven, Germany",
        "BCC":"Beijing Climate Center, Beijing 100081, China",
        "CAMS":"Chinese Academy of Meteorological Sciences, Beijing 100081, China",
        "CAS":"Chinese Academy of Sciences, Beijing 100029, China",
        "CCCR-IITM":"Centre for Climate Change Research, Indian Institute of Tropical Meteorology Pune, Maharashtra 411 008, India",
        "CCCma":"Canadian Centre for Climate Modelling and Analysis, Environment and Climate Change Canada, Victoria, BC V8P 5C2, Canada",
        "CMCC":"Fondazione Centro Euro-Mediterraneo sui Cambiamenti Climatici, Lecce 73100, Italy",
        "CNRM-CERFACS":"CNRM (Centre National de Recherches Meteorologiques, Toulouse 31057, France), CERFACS (Centre Europeen de Recherche et de Formation Avancee en Calcul Scientifique, Toulouse 31057, France)",
        "CSIRO":"Commonwealth Scientific and Industrial Research Organisation, Aspendale, Victoria 3195, Australia",
        "CSIRO-ARCCSS":"CSIRO (Commonwealth Scientific and Industrial Research Organisation, Aspendale, Victoria 3195, Australia), ARCCSS (Australian Research Council Centre of Excellence for Climate System Science). Mailing address: CSIRO, c/o Simon J. Marsland, 107-121 Station Street, Aspendale, Victoria 3195, Australia",
        "CSIRO-COSIMA":"CSIRO (Commonwealth Scientific and Industrial Research Organisation, Australia), COSIMA (Consortium for Ocean-Sea Ice Modelling in Australia). Mailing address: CSIRO, c/o Simon J. Marsland, 107-121 Station Street, Aspendale, Victoria 3195, Australia",
        "DKRZ":"Deutsches Klimarechenzentrum, Hamburg 20146, Germany",
        "DWD":"Deutscher Wetterdienst, Offenbach am Main 63067, Germany",
        "E3SM-Project":"LLNL (Lawrence Livermore National Laboratory, Livermore, CA 94550, USA); ANL (Argonne National Laboratory, Argonne, IL 60439, USA); BNL (Brookhaven National Laboratory, Upton, NY 11973, USA); LANL (Los Alamos National Laboratory, Los Alamos, NM 87545, USA); LBNL (Lawrence Berkeley National Laboratory, Berkeley, CA 94720, USA); ORNL (Oak Ridge National Laboratory, Oak Ridge, TN 37831, USA); PNNL (Pacific Northwest National Laboratory, Richland, WA 99352, USA); SNL (Sandia National Laboratories, Albuquerque, NM 87185, USA). Mailing address: LLNL Climate Program, c/o David C. Bader, Principal Investigator, L-103, 7000 East Avenue, Livermore, CA 94550, USA",
        "EC-Earth-Consortium":"AEMET, Spain; BSC, Spain; CNR-ISAC, Italy; DMI, Denmark; ENEA, Italy; FMI, Finland; Geomar, Germany; ICHEC, Ireland; ICTP, Italy; IDL, Portugal; IMAU, The Netherlands; IPMA, Portugal; KIT, Karlsruhe, Germany; KNMI, The Netherlands; Lund University, Sweden; Met Eireann, Ireland; NLeSC, The Netherlands; NTNU, Norway; Oxford University, UK; surfSARA, The Netherlands; SMHI, Sweden; Stockholm University, Sweden; Unite ASTR, Belgium; University College Dublin, Ireland; University of Bergen, Norway; University of Copenhagen, Denmark; University of Helsinki, Finland; University of Santiago de Compostela, Spain; Uppsala University, Sweden; Utrecht University, The Netherlands; Vrije Universiteit Amsterdam, the Netherlands; Wageningen University, The Netherlands. Mailing address: EC-Earth consortium, Rossby Center, Swedish Meteorological and Hydrological Institute/SMHI, SE-601 76 Norrkoping, Sweden",
        "ECMWF":"European Centre for Medium-Range Weather Forecasts, Reading RG2 9AX, UK",
        "FIO-QLNM":"FIO (First Institute of Oceanography, Ministry of Natural Resources, Qingdao 266061, China), QNLM (Qingdao National Laboratory for Marine Science and Technology, Qingdao 266237, China)",
        "HAMMOZ-Consortium":"ETH Zurich, Switzerland; Max Planck Institut fur Meteorologie, Germany; Forschungszentrum Julich, Germany; University of Oxford, UK; Finnish Meteorological Institute, Finland; Leibniz Institute for Tropospheric Research, Germany; Center for Climate Systems Modeling (C2SM) at ETH Zurich, Switzerland",
        "INM":"Institute for Numerical Mathematics, Russian Academy of Science, Moscow 119991, Russia",
        "IPSL":"Institut Pierre Simon Laplace, Paris 75252, France",
        "KIOST":"Korea Institute of Ocean Science and Technology, Busan 49111, Republic of Korea",
        "LLNL":"Lawrence Livermore National Laboratory, Livermore, CA 94550, USA. Mailing address: LLNL Climate Program, c/o Stephen A. Klein, Principal Investigator, L-103, 7000 East Avenue, Livermore, CA 94550, USA",
        "MESSy-Consortium":"The Modular Earth Submodel System (MESSy) Consortium, represented by the Institute for Physics of the Atmosphere, Deutsches Zentrum fur Luft- und Raumfahrt (DLR), Wessling, Bavaria 82234, Germany",
        "MIROC":"JAMSTEC (Japan Agency for Marine-Earth Science and Technology, Kanagawa 236-0001, Japan), AORI (Atmosphere and Ocean Research Institute, The University of Tokyo, Chiba 277-8564, Japan), NIES (National Institute for Environmental Studies, Ibaraki 305-8506, Japan), and R-CCS (RIKEN Center for Computational Science, Hyogo 650-0047, Japan)",
        "MOHC":"Met Office Hadley Centre, Fitzroy Road, Exeter, Devon, EX1 3PB, UK",
        "MPI-M":"Max Planck Institute for Meteorology, Hamburg 20146, Germany",
        "MRI":"Meteorological Research Institute, Tsukuba, Ibaraki 305-0052, Japan",
        "NASA-GISS":"Goddard Institute for Space Studies, New York, NY 10025, USA",
        "NASA-GSFC":"NASA Goddard Space Flight Center, Greenbelt, MD 20771, USA",
        "NCAR":"National Center for Atmospheric Research, Climate and Global Dynamics Laboratory, 1850 Table Mesa Drive, Boulder, CO 80305, USA",
        "NCC":"NorESM Climate modeling Consortium consisting of CICERO (Center for International Climate and Environmental Research, Oslo 0349), MET-Norway (Norwegian Meteorological Institute, Oslo 0313), NERSC (Nansen Environmental and Remote Sensing Center, Bergen 5006), NILU (Norwegian Institute for Air Research, Kjeller 2027), UiB (University of Bergen, Bergen 5007), UiO (University of Oslo, Oslo 0313) and UNI (Uni Research, Bergen 5008), Norway. Mailing address: NCC, c/o MET-Norway, Henrik Mohns plass 1, Oslo 0313, Norway",
        "NERC":"Natural Environment Research Council, STFC-RAL, Harwell, Oxford, OX11 0QX, UK",
        "NIMS-KMA":"National Institute of Meteorological Sciences/Korea Meteorological Administration, Climate Research Division, Seoho-bukro 33, Seogwipo-si, Jejudo 63568, Republic of Korea",
        "NIWA":"National Institute of Water and Atmospheric Research, Hataitai, Wellington 6021, New Zealand",
        "NOAA-GFDL":"National Oceanic and Atmospheric Administration, Geophysical Fluid Dynamics Laboratory, Princeton, NJ 08540, USA",
        "NTU":"National Taiwan University, Taipei 10650, Taiwan",
        "NUIST":"Nanjing University of Information Science and Technology, Nanjing, 210044, China",
        "PCMDI":"Program for Climate Model Diagnosis and Intercomparison, Lawrence Livermore National Laboratory, Livermore, CA 94550, USA",
        "PNNL-WACCEM":"PNNL (Pacific Northwest National Laboratory), Richland, WA 99352, USA",
        "RTE-RRTMGP-Consortium":"AER (Atmospheric and Environmental Research, Lexington, MA 02421, USA); UColorado (University of Colorado, Boulder, CO 80309, USA). Mailing address: AER c/o Eli Mlawer, 131 Hartwell Avenue, Lexington, MA 02421, USA",
        "RUBISCO":"ORNL (Oak Ridge National Laboratory, Oak Ridge, TN 37831, USA); ANL (Argonne National Laboratory, Argonne, IL 60439, USA); BNL (Brookhaven National Laboratory, Upton, NY 11973, USA); LANL (Los Alamos National Laboratory, Los Alamos, NM 87545); LBNL (Lawrence Berkeley National Laboratory, Berkeley, CA 94720, USA); NAU (Northern Arizona University, Flagstaff, AZ 86011, USA); NCAR (National Center for Atmospheric Research, Boulder, CO 80305, USA); UCI (University of California Irvine, Irvine, CA 92697, USA); UM (University of Michigan, Ann Arbor, MI 48109, USA). Mailing address: ORNL Climate Change Science Institute, c/o Forrest M. Hoffman, Laboratory Research Manager, Building 4500N Room F106, 1 Bethel Valley Road, Oak Ridge, TN 37831-6301, USA",
        "SNU":"Seoul National University, Seoul 08826, Republic of Korea",
        "THU":"Department of Earth System Science, Tsinghua University, Beijing 100084, China",
        "UA":"Department of Geosciences, University of Arizona, Tucson, AZ 85721, USA",
        "UCI":"Department of Earth System Science, University of California Irvine, Irvine, CA 92697, USA",
        "UCSB":"Bren School of Environmental Science and Management, University of California, Santa Barbara. Mailing address: c/o Samantha Stevenson, 2400 Bren Hall, University of California Santa Barbara, Santa Barbara, CA 93106, USA",
        "UHH":"Universitat Hamburg, Hamburg 20148, Germany"
    }

    '''