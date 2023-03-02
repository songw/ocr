import math
import json


rail_types = ['TBJU', 'C64K', 'C70E', 'C64T', 'C70EH']

def extract(result):
    json_result = json.loads(result)
    print(json_result)
    page = json_result.get("pages")
    if page is None:
        return

    lines = page[0].get("lines")
    if lines is None:
        return
    anchor_coords = []
    other_coords = []
    for line in lines:
        print(line['content'])
        words = line.get('words')
        if words is not None:
            for word in words:
                coord0 = word['coord'][0]
                coord3 = word['coord'][3]
                cnt = word['content']
                if cnt in rail_types:
                    anchor_coords.append((coord3['x'], coord3['y'], cnt))
                else:
                    other_coords.append((coord0['x'], coord0['y'], cnt))
    
    cnt = ''
    if (len(other_coords) > 0 and len(anchor_coords) > 0):
        dist_lists = []
        for other_coord in other_coords:
            dist = math.sqrt(math.pow(other_coord[0]-anchor_coords[0][0], 2)+math.pow(other_coord[1]-anchor_coords[0][1], 2))
            dist_lists.append((dist, other_coord[2]))
        
        sorted_dist_lists = sorted(dist_lists)
        
        for dist in sorted_dist_lists:
            cnt += ''.join(filter(str.isdigit,dist[1]))
            if len(cnt) >= 7:
                break
        print(anchor_coords[0][2])
        print(cnt)


def extract_invoice(result):
    with open("result.json", "w") as f:
        f.write(result)
    json_result = json.loads(result)
    page = json_result.get("pages")[0]
    if page is None:
        return

    tables = page.get("tables")
    if tables is None:
        return

    for table in tables:
        cells = table.get("cells")
        if cells is None:
            return 

        for cell in cells:
            row = cell.get("row")
            col = cell.get("col")
            lines = cell.get("lines")
            if lines is not None:
                combine_str = ""
                for line in lines:
                    combine_str += line.get("content")
                print(row, col, combine_str)
            else:
                print(row, col, "")
