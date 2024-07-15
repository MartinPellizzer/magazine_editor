database_filepath = 'magazine_database'
magazine_vol = '2024_07'
magazine_folderpath = f'{database_filepath}/{magazine_vol}'
magazine_pages_foldernames = os.listdir(magazine_folderpath)

page_i = 0
for magazine_page_foldername in magazine_pages_foldernames:
    if magazine_page_foldername == 'cover': continue
    page_i += 1
    
    magazine_page_folderpath = f'{magazine_folderpath}/{magazine_page_foldername}'
    print(magazine_page_folderpath)

    # data    
    json_filepath = f'{magazine_page_folderpath}/data.json'
    with open(json_filepath, 'r', encoding='utf-8') as f: 
        data = json.load(f)

    study_url = data['study_url']
    study_abstract = data['study_abstract']

    if study_abstract.strip() != '':
        print(study_url)
        print('\n')
        print(study_abstract)
        print('\n\n')
        prompt = f'''
            Spiegami questo studio in poche parole come se fossi un principiante.
            Nello specifico, spiegami qual'è il problema, cosa viene usato per risolvere il problema e quali sono i risultati.
        '''
        reply = util_ai.gen_reply(prompt).strip()
        print('\n\n\n\n\n')
        with open('', 'w') as f: f.write(reply)
        time.sleep(g.SLEEP_TIME)

