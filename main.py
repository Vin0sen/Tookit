from BruteForce import BpService

bp = BpService()
host = bp.args.host
type = bp.args.service
bp.attack(host, type)