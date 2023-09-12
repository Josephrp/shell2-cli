# Import the necessary packages
import time,os,json
from prettyprinter import cpprint
import inquirer
from datetime import datetime

import configparser
config = configparser.ConfigParser()
CONFIG_DIR = os.path.expanduser("~/")
CONFIG_FILE = os.path.join(CONFIG_DIR, ".shell2_cli_config")
config.read(CONFIG_FILE)
def get_api_key():
    return config['DEFAULT'].get('apikey', None)

from shell2.client import Shell2Client
shell2_client = Shell2Client( get_api_key() )

def save_json(path,obj):
    with open(path,'w') as fout:
        json.dump(obj, fout)


LLM_OPTIONS = [
    'openai/gpt-3.5-turbo-16k',
    'openai/gpt-4',
    'openai/gpt-3.5-turbo',
    'openai/gpt-4-32k',
    'replicate/replicate/llama-2-70b-chat',
    'replicate/a16z-infra/llama-2-13b-chat',
    'replicate/a16z-infra/llama-2-7b-chat',    
]
KEYSTORE_OPTIONS = [
    'openai',
    'replicate'
]


cpprint('### CLI for shell2.raiden.ai ###')


def selector_sessions():
    def fn_sessionNew():
        print('############### Create a new session ###############')
        
        timeout = 600
        timeout = input('timeout in seconds (default 600) > ')
        multiplayer = input('enable multiplayer (y/n) > ')
        nosync_files = input('upload files in current folder to session ? (max total 500Mb) (y/n) > ')
        voice = input('use voice as message input (experimental) (y/n) > ')
        
        try:
            timeout = int(timeout)
        except Exception as e:
            timeout = 600
        multiplayer = True if ( multiplayer == 'Y' or multiplayer == 'y' ) else False
        nosync_files = False if ( nosync_files == 'Y' or nosync_files == 'y' ) else True
        
        voice = True if ( voice == 'Y' or voice == 'y' ) else False

        cpprint({
            'timeout' : timeout,
            'multiplayer' : multiplayer,
            'nosync_files' : nosync_files,
            'voice' : voice,
        })
        
        cmd_live = f'shell2_cli_live --sandbox session --action new --timeout {timeout}'
        cmd_live += ' --multiplayer' if multiplayer else ''
        cmd_live += ' --nosync' if nosync_files else ''
        cmd_live += ' --voice' if voice else ''
        os.system(cmd_live)

    def fn_sessionResume():
        print('############### Resume a previous sessions ###############')
        response = shell2_client.session.list()
        
        inactive_sessions = [e for e in response['sessions'] if e['done'] ]
        choices_sessions = [ f"{e['sessionId']} | {str( datetime.fromtimestamp( int(e['timestampCreated']/1000) ) )} | "
            + f"{'done' if e['done'] else 'still open'}"
            for e in inactive_sessions
        ] + ['back to menu']
        
        questions = [
            inquirer.List(
                "sessionId",
                message="session",
                choices=choices_sessions,
            ),
        ]

        choice_sessionId = inquirer.prompt(questions)
        if choice_sessionId['sessionId'] != 'back to menu':
            selected_sessionId = choice_sessionId['sessionId'].split(' | ')[0].strip()

            timeout = 600
            
            timeout = input('timeout in seconds (default 600) > ')
            multiplayer = input('enable multiplayer (y/n) > ')
            nosync_files = input('upload files in current folder to session ? (max total 500Mb) (y/n) > ')
            voice = input('use voice as message input (experimental) (y/n) > ')
            
            try:
                timeout = int(timeout)
            except Exception as e:
                timeout = 600
            multiplayer = True if ( multiplayer == 'Y' or multiplayer == 'y' ) else False
            nosync_files = False if ( nosync_files == 'Y' or nosync_files == 'y' ) else True
            voice = True if ( voice == 'Y' or voice == 'y' ) else False

            cpprint({
                'sessionId' : selected_sessionId,
                'timeout' : timeout,
                'multiplayer' : multiplayer,
                'nosync_files' : nosync_files,
                'voice' : voice,
            })
            
            cmd_live = f'shell2_cli_live --sandbox session --action resume --sessionId {selected_sessionId} --timeout {timeout}'
            cmd_live += ' --multiplayer' if multiplayer else ''
            cmd_live += ' --nosync' if nosync_files else ''
            cmd_live += ' --voice' if voice else ''
            os.system(cmd_live)
        
        
    def fn_sessionPrevious():
        print('############### Previous sessions ###############')
        response = shell2_client.session.list()
        
        choices_sessions = [ f"{e['sessionId']} | {str( datetime.fromtimestamp( int(e['timestampCreated']/1000) ) )} | "
            + f"{'done' if e['done'] else 'still open'}"
            for e in response['sessions']
        ] + ['back to menu']
        
        questions = [
            inquirer.List(
                "sessionId",
                message="session",
                choices=choices_sessions,
            ),
        ]

        choice_sessionId = inquirer.prompt(questions)
        if choice_sessionId['sessionId'] != 'back to menu':
            selected_sessionId = choice_sessionId['sessionId'].split(' | ')[0].strip()
            response_session = shell2_client.session.get({"sessionId" : selected_sessionId})
            
            save_json(
                os.path.join(os.getcwd(), f'sessionId_{selected_sessionId}.json'),
                response_session
            )
            
            cpprint({
                'sessionId' : selected_sessionId,
                'saved' : f"./sessionId_{selected_sessionId}.json"
            })
            
            
            input('\n< back\n')
        
    def fn_sessionJoin():
        print('############### Join an active session ###############')
        response = shell2_client.session.list()
        
        active_sessions = [e for e in response['sessions'] if not e['done'] ]
        
        choices_sessions = [ f"{e['sessionId']} | {str( datetime.fromtimestamp( int(e['timestampCreated']/1000) ) )} | "
            + f"{'done' if e['done'] else 'still open'}"
            for e in active_sessions
        ] + ['back to menu']
        
        questions = [
            inquirer.List(
                "sessionId",
                message="session",
                choices=choices_sessions,
            ),
        ]

        choice_sessionId = inquirer.prompt(questions)
        if choice_sessionId['sessionId'] != 'back to menu':
            selected_sessionId = choice_sessionId['sessionId'].split(' | ')[0].strip()

            nosync_files = input('upload files in current folder to join session ? (max total 500Mb) (y/n) > ')
            nosync_files = False if ( nosync_files == 'Y' or nosync_files == 'y' ) else True
            voice = input('use voice as message input (experimental) (y/n) > ')
            voice = True if ( voice == 'Y' or voice == 'y' ) else False

            cpprint({
                'sessionId' : selected_sessionId,
                'nosync_files' : nosync_files,
                'voice': voice,
            })

            cmd_live = f'shell2_cli_live --sandbox session --action join --sessionId {selected_sessionId}'
            cmd_live += ' --nosync' if nosync_files else ''
            cmd_live += ' --voice' if voice else ''
            os.system(cmd_live)
        else:
            selector_sessions()


    def fn_sessionMultiplayer():
        print('############### Join an multiplayer session ###############')
        
        choices_multiplayer_method = [
            'i have a multiplayer url (like http://shell2.raiden.ai/view/sequence/user@email.com/12345-abcde )',
            'i have a session owner email and sessionId',
            'back to menu',
        ]
        
        questions = [
            inquirer.List(
                "multiplayer_method",
                message="multiplayer session",
                choices=choices_multiplayer_method,
            ),
        ]

        choice_method = inquirer.prompt(questions)
        chosen_method = choice_method['multiplayer_method']
        if chosen_method == 'i have a multiplayer url (like http://shell2.raiden.ai/view/sequence/user@email.com/12345-abcde )':
          
            multiplayer_url = input('paste multiplayer url > ')
            nosync_files = input('upload files in current folder to session ? (max total 500Mb) (y/n) > ')
            nosync_files = False if ( nosync_files == 'Y' or nosync_files == 'y' ) else True
            voice = input('use voice as message input (experimental) (y/n) > ')
            voice = True if ( voice == 'Y' or voice == 'y' ) else False


            cpprint({
                'multiplayer_url' : multiplayer_url,
                'nosync_files' : nosync_files,
                'voice' : voice,
            })

            cmd_live = f'shell2_cli_live --sandbox session --action join --link {multiplayer_url.strip()}'
            cmd_live += ' --nosync' if nosync_files else ''
            cmd_live += ' --voice' if voice else ''
            os.system(cmd_live)
            
        elif chosen_method == 'i have a session owner email and sessionId':
        
            session_owner = input('session owner email > ')
            sessionId = input('sessionId > ')
            nosync_files = input('upload files in current folder to session ? (max total 500Mb) (y/n) > ')
            nosync_files = False if ( nosync_files == 'Y' or nosync_files == 'y' ) else True

            voice = input('use voice as message input (experimental) (y/n) > ')
            voice = True if ( voice == 'Y' or voice == 'y' ) else False

            cpprint({
                'session_owner' : session_owner,
                'sessionId' : sessionId,
                'nosync_files' : nosync_files,
                'voice' : voice,
            })

            cmd_live = f'shell2_cli_live --sandbox session --action join --user {session_owner.strip()} --sessionId {sessionId.strip()}'
            cmd_live += ' --nosync' if nosync_files else ''
            cmd_live += ' --voice' if voice else ''
            os.system(cmd_live)
        
        elif chosen_method == 'back to menu':
            selector_sessions()
    
    
    sessionsMenu = [
        'create a new session' ,
        'join an active session' ,
        'join a multiplayer session' ,
        'resume a previous session' ,
        'view & save previous sessions data to json' ,
        'back to menu'
    ]
    questions_sessionsMenu = [
        inquirer.List(
            "sessions_task",
            message="sessions task",
            choices=sessionsMenu,
        ),
    ]

    choice_sessionsMenu = inquirer.prompt(questions_sessionsMenu)
    selected_sessionsMenu = choice_sessionsMenu['sessions_task']

    if selected_sessionsMenu == 'create a new session' :
        fn_sessionNew()
    elif selected_sessionsMenu == 'join an active session' :
        fn_sessionJoin()
    elif selected_sessionsMenu == 'resume a previous session' :
        fn_sessionResume()
    elif selected_sessionsMenu == 'join a multiplayer session' :
        fn_sessionMultiplayer()
    elif selected_sessionsMenu == 'view & save previous sessions data to json':
        fn_sessionPrevious()
        selector_sessions()
    elif selected_sessionsMenu == 'back to menu':
        selector_root()



def selector_sequences():
    def fn_sequenceRun():
        print('############### Run a new sequence ###############')
        print('\nto a run a sequence, you need to have a `sequence.txt` file in your current folder')
        print('the file should contain a list of steps, separated by an empty line')
        print('\nexample of a `sequence.txt` file :')
        print('```')
        print('/doc https://raw.githubusercontent.com/raidendotai/shell2-example-data/main/mlb_2012.csv')
        print('\nplot the top 5 teams and their wins in a bar chart, in a png file')
        print('```\n')
        
        input('> continue ?')
        sequenceRunMenu = [ 'i have created the `sequence.txt` file' , 'back to menu']
        questions_sequenceRunMenu = [
            inquirer.List(
                "sequence_run_task",
                message="sequences run task",
                choices=sequenceRunMenu,
            ),
        ]
            
        choice_sequenceRunMenu = inquirer.prompt(questions_sequenceRunMenu)
        selected_sequenceRunMenu = choice_sequenceRunMenu['sequence_run_task']
        
        if selected_sequenceRunMenu == 'i have created the `sequence.txt` file':
            timeout = 600
            timeout = input('timeout in seconds (default 600) > ')
            #multiplayer = input('enable multiplayer (y/n) > ')
            nosync_files = input('upload files in current folder with sequence ? (max total 500Mb) (y/n) > ')
            try:
                timeout = int(timeout)
            except Exception as e:
                timeout = 600
            #multiplayer = True if ( multiplayer == 'Y' or multiplayer == 'y' ) else False
            nosync_files = False if ( nosync_files == 'Y' or nosync_files == 'y' ) else True

            cpprint({
                'timeout' : timeout,
                'nosync_files' : nosync_files,
            })
            
            cmd_live = f'shell2_cli_live --sandbox sequence --action run --timeout {timeout}'
            cmd_live += ' --nosync' if nosync_files else ''
            os.system(cmd_live)

        elif selected_sequenceRunMenu == 'back to menu':
            selector_root()
    def fn_sequencePrevious():
        print('############### Previous sequences ###############')
        response = shell2_client.sequence.list()
        
        choices_sequences = [ f"{e['sequenceId']} | {str( datetime.fromtimestamp( int(e['timestampCreated']/1000) ) )} | "
            + f"{'done' if e['done'] else 'running'}"
            + f" | {e['sequence'][0][0:30]} ..."
            for e in response['sequences']
        ] + ['back to menu']
        
        #cpprint(response)
        print('\nChoose a sequence, the data json will be saved under the current folder\n')
        
        questions = [
            inquirer.List(
                "sequenceId",
                message="sequence",
                choices=choices_sequences,
            ),
        ]

        choice_sequenceId = inquirer.prompt(questions)
        if choice_sequenceId['sequenceId'] != 'back to menu':
            selected_sequenceId = choice_sequenceId['sequenceId'].split(' | ')[0].strip()
            response_sequence = shell2_client.sequence.get({"sequenceId" : selected_sequenceId})

            save_json(
                os.path.join(os.getcwd(), f'sequenceId_{selected_sequenceId}.json'),
                response_sequence
            )
            
            cpprint({
                'sequenceId' : selected_sequenceId,
                'saved' : f"./sequenceId_{selected_sequenceId}.json"
            })
            
            
            input('\n< back\n')
        
    
    sequencesMenu = [ 'run a new sequence' , 'view & save previous sequences to json' , 'back to menu']
    questions_sequencesMenu = [
        inquirer.List(
            "sequences_task",
            message="sequences task",
            choices=sequencesMenu,
        ),
    ]

    choice_sequencesMenu = inquirer.prompt(questions_sequencesMenu)
    selected_sequencesMenu = choice_sequencesMenu['sequences_task']

    if selected_sequencesMenu == 'run a new sequence':
        fn_sequenceRun()
    if selected_sequencesMenu == 'view & save previous sequences to json':
        fn_sequencePrevious()
        selector_sequences()
    elif selected_sequencesMenu == 'back to menu':
        selector_root()

def selector_settings():
    def fn_settingsGet():
        print('############### Current Settings ###############')
        response = shell2_client.settings.get()
        settings = response['settings']
        cpprint(settings)
        input('\n< back\n')
    def fn_settingsChangeLLM():
        print('############### Change LLM ###############')
        response = shell2_client.settings.get()
        current_llm = response['settings']['llm']
        
        cpprint({
            'llm' : current_llm
        })
        
        input('\nwhen changing LLM, make sure you have stored a relevant API keys for the model > got it')
        
        choices_llm = LLM_OPTIONS + ['back to menu']

        questions = [
            inquirer.List(
                "llm",
                message="LLM (make sure you have stored relevant API keys)",
                choices=choices_llm,
            ),
        ]

        choice_llm = inquirer.prompt(questions)
        if choice_llm['llm'] != 'back to menu':
            selected_llm = choice_llm['llm']
            response_settings_update = shell2_client.settings.update({"llm" : selected_llm})
            
            cpprint({
                'llm' : response_settings_update['settings']['llm']
            })
            
            input('\n< back\n')
    
    def fn_settingsUpdateKeystore():
        print('############### Update Keystore ###############')
        response = shell2_client.settings.get()
        current_keystore = response['settings']['keystore']
        cpprint({
            'keystore' : current_keystore
        })
        
        input('\nstore your API keys that will be used by your chosen language models.\nall your api keys are safely stored and wrapped in 2 encryption layers > got it')
    
        choices_keystore_api = KEYSTORE_OPTIONS + ['back to menu']

        questions = [
            inquirer.List(
                "api_key",
                message="API Key (will be encrypted in storage)",
                choices=choices_keystore_api,
            ),
        ]

        choice_keystore_api = inquirer.prompt(questions)
        if choice_keystore_api['api_key'] != 'back to menu':
            selected_keystore_api = choice_keystore_api['api_key']
            
            user_api_key = input(f'paste your API key for {selected_keystore_api} > ')
            
            keystore_obj = {}
            keystore_obj[ selected_keystore_api ] = user_api_key.strip()
            
            response_settings_update = shell2_client.settings.update({
                "keystore" : keystore_obj
            })
            
            cpprint({
                "keystore" : response_settings_update['settings']['keystore']
            })
            input('\n< back\n')
    
    settingsMenu = [ 'current settings' , 'change language model' , 'configure API keys (for openai, etc)' , 'back to menu']
    questions_settingsMenu = [
        inquirer.List(
            "settings_task",
            message="settings",
            choices=settingsMenu,
        ),
    ]

    choice_settingsMenu = inquirer.prompt(questions_settingsMenu)
    selected_settingsMenu = choice_settingsMenu['settings_task']

    if selected_settingsMenu == 'current settings':
        fn_settingsGet()
        selector_root()
    if selected_settingsMenu == 'change language model':
        fn_settingsChangeLLM()
        selector_root()
    if selected_settingsMenu == 'configure API keys (for openai, etc)':
        fn_settingsUpdateKeystore()
        selector_root()
    elif selected_settingsMenu == 'back to menu':
        selector_root()

def selector_root():
    rootMenu = [ 'session', 'sequence' , 'settings'  , 'exit' ]
    questions_rootMenu = [
        inquirer.List(
            "task",
            message="task",
            choices=rootMenu,
        ),
    ]

    choice_rootMenu = inquirer.prompt(questions_rootMenu)
    selected_rootMenu = choice_rootMenu['task']
    #print(selected_rootMenu)
    if selected_rootMenu == 'session': selector_sessions()
    elif selected_rootMenu == 'sequence': selector_sequences()
    elif selected_rootMenu == 'settings': selector_settings()
    else:
        exit(0)

def main():
    selector_root()
if __name__ == '__main__':
    main()