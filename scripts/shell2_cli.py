import argparse
import configparser
import os
import json
from prettyprinter import cpprint


config = configparser.ConfigParser()
CONFIG_DIR = os.path.expanduser("~/")
CONFIG_FILE = os.path.join(CONFIG_DIR, ".shell2_cli_config")
config.read(CONFIG_FILE)

def _save_json(path,obj):
    with open(path,'w') as fout:
        json.dump(obj, fout)

def set_key(apikey):
    config['DEFAULT']['apikey'] = apikey
    with open(CONFIG_FILE, 'w') as configfile:
        config.write(configfile)

def get_key():
    return config['DEFAULT'].get('apikey', None)

def main():

    parser = argparse.ArgumentParser(description='CLI for shell2.raiden.ai')
    parser.add_argument('--key', help='set your shell2.raiden.ai api key')
    
    #session stuff
    parser.add_argument('--session', action='store_true', help='start/resume/join/multiplayer a shell2 session')
    parser.add_argument('--new', action='store_true', help='')
    parser.add_argument('--resume', action='store_true', help='')
    parser.add_argument('--join', action='store_true', help='')
    parser.add_argument('--multiplayer', action='store_true', help='enable multiplayer; used with --new or --resume')
    
    parser.add_argument('--sessionId', type=str)
    parser.add_argument(
        '--url',
        type=str,
        help='link to a shared multiplayer session (example : `https://shell2.raiden.ai/view/session/user@email.com/exampleid-123456` )'
    )
    parser.add_argument('--user', type=str)
    parser.add_argument('--voice', action='store_true', help='use voice commands as message input for sessions')
    
    #sequence stuff
    parser.add_argument('--sequence', action='store_true', help='run a sequence predefined in sequence.txt in current folder')
    parser.add_argument('--run', action='store_true', help='')
    parser.add_argument('--webhook', type=str, help='webhook url for sequence')
    parser.add_argument('--sequenceId', type=str)
    
    #general stuff
    parser.add_argument(
        '--nosync',
        action='store_true',
        required=False,
        help='! without this parameter, your current folder files will be uploaded to the shell2 session/sequence by default (max 500 Mb) !'
    )
    parser.add_argument('--timeout', type=int, help='timeout in seconds for created/resumed sessions and created sequences')    

    parser.add_argument('--dump', action='store_true', help='save session/sequence data in a json file. require --sessionId or --sequenceId')

    args = parser.parse_args()
    
    if args.key:
        set_key(args.key)
        print('shell2.raiden.ai api key stored :', args.key)
        print('you can now run the `shell2` command')
        return 0
    
    
    #############################################
    apikey = get_key()
    if not apikey:
        print('no api key found. first run `shell2 --key YOUR_API_KEY` to set an api key.')
        return 0
    
    
    
    if (not args.session) and (not args.sequence) :
        os.system('shell2_cli_menu')
    else:
        from shell2.client import Shell2Client
        SHELL2_CLIENT = Shell2Client( get_key() )
        
        print('make sure you read the docs at shell2.raiden.ai')
        print('if you do not use the --nosync parameter, the content of your current folder will be uploaded to the sandbox (max 500 Mb)\n')
        
        print('in sessions, remember to close your sessions using the `/done` command !\n')
    
        timeout = 600
        if args.timeout:
            timeout = args.timeout
            
            
        if args.session:
            if args.dump and args.sessionId:
                response_session = SHELL2_CLIENT.session.get({"sessionId" : args.sessionId})
                _save_json(
                    os.path.join(os.getcwd(), f'sessionId_{args.sessionId}.json'),
                    response_session
                )
                cpprint({
                    'sessionId' : args.sessionId,
                    'saved' : f"./sessionId_{args.sessionId}.json"
                })
                exit(0)
        
            if (not args.new) and (not args.resume) and (not args.join) and (not args.url) :
                cmd_live = f'shell2_cli_live --sandbox session --action new --timeout {timeout}'
                cmd_live += ' --multiplayer' if args.multiplayer else ''
                cmd_live += ' --nosync' if args.nosync else ''
                cmd_live += ' --voice' if args.voice else ''
                
                os.system(cmd_live)
           
            elif (not args.new) and (not args.resume) and (not args.join) and (args.url):
                # shell2 --session --url {url}
                cmd_live = f'shell2_cli_live --sandbox session --action join --link {args.url}'
                cmd_live += ' --nosync' if args.nosync else ''
                cmd_live += ' --voice' if args.voice else ''
                os.system(cmd_live)     
            else:
                if args.new:
                    multiplayer_mode = ' --multiplayer' if args.multiplayer else ''
                    cmd_live = f'shell2_cli_live --sandbox session --action new --timeout {timeout}{multiplayer_mode}'
                    cmd_live += ' --nosync' if args.nosync else ''
                    cmd_live += ' --voice' if args.voice else ''
                    os.system(cmd_live)
                elif args.resume:
                    multiplayer_mode = ' --multiplayer' if args.multiplayer else ''
                    cmd_live = f'shell2_cli_live --sandbox session --action resume --sessionId "{args.sessionId}" --timeout {timeout}{multiplayer_mode}'
                    cmd_live += ' --nosync' if args.nosync else ''
                    cmd_live += ' --voice' if args.voice else ''
                    os.system(cmd_live)
                elif args.join:
                    if args.url:
                        cmd_live = f'shell2_cli_live --sandbox session --action join --link "{args.url}"'
                        cmd_live += ' --nosync' if args.nosync else ''
                        cmd_live += ' --voice' if args.voice else ''
                        os.system(cmd_live)
                    elif args.user and args.sessionId:
                        cmd_live = f'shell2_cli_live --sandbox session --action join --sessionId "{args.sessionId}" --user "{args.user}"'
                        cmd_live += ' --nosync' if args.nosync else ''
                        cmd_live += ' --voice' if args.voice else ''
                        os.system(cmd_live)
                    
                    
        elif args.sequence:
        
            if args.dump and args.sequenceId:
                response_sequence = SHELL2_CLIENT.sequence.get({"sequenceId" : args.sequenceId})
                _save_json(
                    os.path.join(os.getcwd(), f'sequenceId_{args.sequenceId}.json'),
                    response_sequence
                )
                cpprint({
                    'sequenceId' : args.sequenceId,
                    'saved' : f"./sequenceId_{args.sequenceId}.json"
                })
                exit(0)
        
            if not args.run :
                cmd_live = f'shell2_cli_live --sandbox sequence --action run --timeout {timeout}'
                cmd_live += f' --webhook {args.webhook}' if args.webhook else ''
                cmd_live += ' --nosync' if args.nosync else ''
                os.system(cmd_live)
            else:
                if args.run:
                    cmd_live = f'shell2_cli_live --sandbox sequence --action run --timeout {timeout}'
                    cmd_live += ' --nosync' if args.nosync else ''
                    cmd_live += f' --webhook {args.webhook}' if args.webhook else ''
                    os.system(cmd_live)
        else:
            print('bad format; check docs at shell2.raiden.ai')
    

if __name__ == '__main__':
    main()