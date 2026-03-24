structure_netze_strom_1 = """
- Strom
  - Anmeldung E-Ladestation
  - Netzanschluss
  - Netzzugang & Verträge
"""
structure_netze_strom_2 = """
- Strom
  - Netznutzungsentgelte
  - Netzstrukturdaten
"""
structure_netze_strom_3 = """
- Strom
  - Grund- & Ersatzversorgung
  - EEG & Einspeiser
"""
structure_netze_erdgas_1 = """
- Erdgas
  - Netzanschluss
  - Netzzugang & Verträge
  - Netznutzungsentgelte
"""
structure_netze_erdgas_2 ="""
- Erdgas (main page)
  - Netznutzungsentgelte (sub page, make sure click to enter this sub page)
  - Netzstrukturdaten (sub page, make sure click to enter this sub page)
"""
structure_netze_erdgas_3 ="""
- Erdgas (main page)
  - Grund- & Ersatzversorgung (sub page, make sure click to enter this sub page)
"""
structure_netze_wasser = """
- Wasser (everything on this webpage)
"""
structure_netze_glasfaser = """
- Glasfaser
"""
strucutre_netze_messstellenbetrieb ="""
- Messstellenbetrieb
"""
strucutre_netze_planauskunft = """
- Planauskunft (zum Button 'Zur Planauskunft' musst du Info geben, dass es ein Formular gibt)
"""

structure_unternehmen ="""
- Unternehmen
"""
structure_karriere ="""
- Karriere
"""
structure_aktuelles ="""
- Aktuelles
"""
structure_kontakt ="""
- Kontakt
"""
structure_Kundenportal ="""
- Kundenportal (Hier musst du info geben, was das Kundenportal anbietet)
"""

#[structure_netze_strom_1, structure_netze_strom_2, structure_netze_strom_3, structure_netze_erdgas_1, structure_netze_erdgas_2, structure_netze_was_glas, strucutre_netze_mess_plan]

structure_ = {
    "Netze-Strom": {
        "url": "https://www.stadtwerke-waiblingen.de/Netze/Stromnetz",
        "subpart": [structure_netze_strom_3],

    },
}
structure = {
    "Kundenportal": {
        "url": "https://privatkundenportal.net/waiblingen/",
        "subpart": [structure_Kundenportal],

    },
}