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
- Erdgas
  - Netzstrukturdaten
  - Grund- & Ersatzversorgung
"""
structure_netze_was_glas = """
- Wasser
- Glasfaser
"""
strucutre_netze_mess_plan ="""
- Messstellenbetrieb
- Planauskunft
  - Zur Planauskunft
"""

structure_unternehmen ="""
- Unternehmen
"""
structure = {
    "Netze-Strom": {
        "url": "https://www.stadtwerke-waiblingen.de/Netze/Uebersicht-Netze",
        "subpart": [structure_netze_strom_1, structure_netze_strom_2, structure_netze_strom_3, structure_netze_erdgas_1, structure_netze_erdgas_2, structure_netze_was_glas, strucutre_netze_mess_plan],

    },
    "Unternehmen": {
        "url": "https://www.stadtwerke-waiblingen.de/unternehmen",
        "subpart": [structure_unternehmen]
    }
}