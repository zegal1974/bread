Attributes:

| Attribute          | Type        | Description                                                                                                                                 |
|--------------------|-------------|---------------------------------------------------------------------------------------------------------------------------------------------|
| add_paused         | bool        | Add the torrent in a paused state.                                                                                                          | 
| auto_managed       | bool        | Set torrent to auto managed mode, i.e. will be started or queued automatically.                                                             |
| download_location  | str         | The path for the torrent data to be stored while downloading.                                                                               |               
| file_priorities    | list of int | The priority for files in torrent, range is [0..7] however, only [0, 1, 4, 7] are normally used and correspond to [Skip, Low, Normal, High] |
| mapped_files       | dict        | A mapping of the renamed filenames in 'index:filename' pairs.                                                                               |
| max_connections    | int         | Sets the maximum number of connections this torrent will open. This must be at least 2. The default is unlimited (-1).                      |
| max_download_slots | int         | Sets the maximum number of peers that are unchoked at the same time on this torrent. This defaults to unlimited (-1).                       |max_download_speed (float): Will limit the download bandwidth used by this torrent to the

limit you set.The default is unlimited (-1) but will not exceed global limit.
max_upload_slots (int): Sets the maximum number of peers that are
unchoked at the same time on this torrent. This defaults to infinite (-1).
max_upload_speed (float): Will limit the upload bandwidth used by this torrent to the limit
you set. The default is unlimited (-1) but will not exceed global limit.
move_completed (bool): Move the torrent when downloading has finished.
move_completed_path (str): The path to move torrent to when downloading has finished.
name (str): The display name of the torrent.
owner (str): The user this torrent belongs to.
pre_allocate_storage (bool): When adding the torrent should all files be pre-allocated.
prioritize_first_last_pieces (bool): Prioritize the first and last pieces in the torrent.
remove_at_ratio (bool): Remove the torrent when it has reached the stop_ratio.
seed_mode (bool): Assume that all files are present for this torrent (Only used when adding a torent).
sequential_download (bool): Download the pieces of the torrent in order.
shared (bool): Enable the torrent to be seen by other Deluge users.
stop_at_ratio (bool): Stop the torrent when it has reached stop_ratio.
stop_ratio (float): The seeding ratio to stop (or remove) the torrent at.
super_seeding (bool): Enable super seeding/initial seeding.