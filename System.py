def launch(recMapInfo,recUavStatus):
	sendUavStatus = []
	time = recUavStatus["time"]
	h_low  = recMapInfo["h_low"]
	h_high = recMapInfo["h_high"]
	if time==0:
		uavs = recMapInfo["init_UAV"]
		for uav in uavs:
			sendUav = oneLaunch(uav)
			sendUavStatus.append(sendUav)
	else:
		uavs = recUavStatus["UAV_we"]
		for uav in uavs:
			z = uav["z"]
			if z<h_low:
				sendUav = oneLaunch(uav)
				if(uav["status"]==0):
					sendUav["z"] = uav["z"]+1
					if inCollisionAll(sendUav,sendUavStatus):
						sendUav["z"] = uav["z"]
					
				
			else:
				#sendUav = searchGoods()
				pass

			sendUavStatus.append(sendUav)	

	return sendUavStatus

def oneLaunch(uav):
	sendUav = {}
	sendUav["no"] = uav["no"]
	sendUav["x"] = uav["x"]
	sendUav["y"] = uav["y"]
	sendUav["goods_no"] = uav["goods_no"]
	sendUav["z"] = uav["z"]

	return sendUav


def up():
	pass

def inCollisionAll(uav_a,uavs):
	for uav in uavs:
		if inCollision(uav_a,uav):
			return True
	return False


def searchGoods(recMapInfo,recUavStatus):
	time = recUavStatus["time"]
	all_goods = recUavStatus["goods"]
	#for goods in all_goods:
		


def inCollision(uav_a,uav_b):
	xa = uav_a["x"]
	ya = uav_a["y"]
	za = uav_a["z"]
	xb = uav_b["x"]
	yb = uav_b["y"]
	zb = uav_b["z"]

	if xa==xb and ya==yb and za==zb:
		return True
	else :
		return False